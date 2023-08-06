"""
The qiprofile imaging Mongodb data model.
"""

import re
import decimal
from numbers import Number
import mongoengine
from mongoengine import (fields, signals, ValidationError)
from .common import (Encounter, Outcome, TumorExtent)


class Point(mongoengine.EmbeddedDocument):
    """The 3D point in the volume voxel space."""

    x = fields.IntField()
    """
    The x dimension value in the image coordinate system.
    """

    y = fields.IntField()
    """
    The y dimension value in the image coordinate system.
    """

    z = fields.IntField()
    """
    The z dimension value in the image coordinate system.
    """


class Image(mongoengine.EmbeddedDocument):
    """The image file encapsulation."""

    meta = dict(allow_inheritance=True)

    name = fields.StringField(required=True)
    """
    The image file base name. The client has the responsibility
    of determining the image file based on the image store. For example,
    a NIfTI scan volume XNAT 1.6 archive 3D volume image location is as
    # follows::

          /path/to/archive/<project>/arc001/<experiment>/SCANS/<scan>/NIFTI/<name>

      where:

      * *project* is the XNAT project name
      * *experiment* is the XNAT experiment label
      * *scan* is the scan number
      * *name* is the volume image file base name
    """

    metadata = fields.DictField()
    """Additional image properties, e.g. average intensity."""


class LabelMap(Image):
    """A label map with an optional associated color lookup table."""

    color_table = fields.StringField()
    """
    The color map lookup table file base name relative to the XNAT
    archive ROI resource location.
    """


class Region(mongoengine.EmbeddedDocument):
    """The 3D region in volume voxel space."""

    mask = fields.EmbeddedDocumentField(Image)
    """
    The binary mask file relative to the image store ROI resource
    location.
    """

    resource = fields.StringField(required=True)
    """The region imaging store resource name, e.g. ``roi``."""

    label_map = fields.EmbeddedDocumentField(LabelMap)
    """The region overlay :class:`LabelMap` object."""

    centroid = mongoengine.EmbeddedDocumentField(Point)
    """The region centroid."""


class Resource(mongoengine.EmbeddedDocument):
    """The image store file access abstraction."""

    meta = dict(allow_inheritance=True)

    name = fields.StringField(required=True)
    """The image store name used to access the resource."""


class SingleImageResource(Resource):
    """A resource with one file."""

    meta = dict(allow_inheritance=True)

    image = fields.EmbeddedDocumentField(Image)
    """The sole resource image."""


class MultiImageResource(Resource):
    """A resource with several files."""

    meta = dict(allow_inheritance=True)

    images = fields.ListField(
        field=fields.EmbeddedDocumentField(Image)
    )
    """The resource images."""


class ImageSequence(Outcome):
    """The Scan or Registration."""

    meta = dict(allow_inheritance=True)

    time_series = fields.EmbeddedDocumentField(SingleImageResource)
    """The 4D time series resource."""

    volumes = fields.EmbeddedDocumentField(MultiImageResource)
    """The 3D volumes resource."""


class Protocol(mongoengine.Document):
    """
    The image acquisition or processing protocol abstract class.
    """

    meta = dict(allow_inheritance=True, collection='qiprofile_protocol')

    technique = fields.StringField(required=True)
    """
    The acquisition or processing technique, e.g. ``T1`` for a
    T1-weighted scan or ``ANTs`` for an ANTs registration.

    The REST update client is responsible for ensuring that technique
    synonyms resolve to the same technique value, e.g. scans with
    descriptions including ``T1`` and ``T1 AXIAL`` should both resolve
    to technique ``T1``. The acquisition and processing details are
    stored in the configuration rather than embedded in the technique.

    Protocol common constraints
    ---------------------------

    Clients are required to enforce the following constraints:

    * Protocols are unique and immutable. Clients are required
      to search for an existing protocol with the same content prior
      to creating a new ``Protocol`` database object.

    * Protocol techniques are disjoint by referencing class, i.e.
      a technique value cannot occur in protocol database objects
      referenced by instances of different classes. For example,
      a `Registration`` instance cannot reference a protocol
      with technique ``T2``, since that is a scan protocol reserved
      technique per the specialization constraints below.

    Protocol specialization constraints
    -----------------------------------

    **Scan**

    Scans with the same protocol and image dimensions are directly
    comparable, e.g. in comparing modeling results across subjects
    or sessions.

    The recommended technique controlled values include, but are not
    limited to, the following:
    * ``T1`` - T1-weighted
    * ``T2`` - T2-weighted
    * ``DW`` - diffusion-weighted
    * ``PD`` - proton density
    """

    configuration = fields.DictField()
    """
    The acquisition or processing input parameter
    {*section*\ : {*option*\ : *value*\ }} dictionary,
    e.g.::

        {
          'FLIRT': {'bins': 640, 'cost_func': 'normcorr'},
          'FNIRT' : {'in_fwhm': [10,6,2,2], 'ref_fwhm': [10,6,2,2]}
        }

    The acquisition configuration is gathered from the PACS and
    should contain parameters of interest for display or inference.

    The processing configuration is gathered from the pipeline and
    should be sufficient for reproducing the result in the context
    of the pipeline. The sections are pipeline task interfaces or
    other pipeline input groupings.

    :Note: MongoDB does not permit dotted dictionary keys. Thus, e.g.,
         'fsl.FNIRT' is not allowed in the preceding example.
    """


class Registration(ImageSequence):
    """
    The patient image registration that results from processing a scan.
    """

    protocol = fields.ReferenceField(Protocol, required=True)
    """The registration protocol."""


class Scan(ImageSequence):
    """
    The the concrete subclass of the abstract :class:`ImageSequence`
    class for scans.
    """

    number = fields.IntField(required=True)
    """
    The scan number. In the XNAT image store, each scan is
    identified by a number unique within the session.
    """

    protocol = fields.ReferenceField(Protocol, required=True)
    """The scan acquisition protocol."""

    bolus_arrival_index = fields.IntField()
    """
    The bolus arrival volume index, or None if this is not a
    DCE scan.
    """

    rois = fields.ListField(field=fields.EmbeddedDocumentField(Region))
    """
    The image regions of interest. For a scan with ROIs, there is
    one ROI per scan tumor. The rois list order is the same as the
    :class:`qirest-client.model.clinical.PathologyReport`
    ``tumors`` list order.
    """

    registrations = fields.ListField(
        field=fields.EmbeddedDocumentField(Registration)
    )
    """
    The registrations performed on the scan.
    """


class Modeling(Outcome):
    """
    The pharmicokinetic modeling run on an image sequence.
    """

    class ParameterResult(mongoengine.EmbeddedDocument):
        """The output for a given modeling run result parameter."""

        image = fields.EmbeddedDocumentField(Image)
        """
        The voxel-wise mapping file name relative to the XNAT
        modeling archive resource location. The image metadata
        should include *average*, the average modeling result
        value across all voxels.
        """

        label_map = fields.EmbeddedDocumentField(LabelMap)
        """The label map overlay NIfTI file."""

    class Source(mongoengine.EmbeddedDocument):
        """
        This Modeling.Source embedded class works around the following
        mongoengine limitation:

        * mongoengine does not allow heterogeneous collections, i.e.
          a domain model Document subclass cannot have subclasses.
          Furthermore, the domain model Document class cannot be
          an inner class.

        Consequently, the Modeling.source field cannot represent an
        abstract superclass with subclasses RegistrationSource
        and ScanSource. The work-around is to introduce this Source
        embedded document disambiguation by creating a disjunction
        object that can either hold a *scan* reference or a
        *registration* reference.
        """

        scan = fields.ReferenceField(Protocol)

        registration = fields.ReferenceField(Protocol)

    protocol = fields.ReferenceField(Protocol, required=True)
    """The modeling protocol."""

    source = fields.EmbeddedDocumentField(Source, required=True)
    """
    The modeling source protocol.

    Since a given :class`Session` contains only one :class:`ImageSequence`
    per source protocol, the image sequence on which modeling is performed
    is determined by the source protocol. Specifying the source as a
    protocol rather than the specific scan or registration allows modeling
    to be embedded in the :class`Session` document rather than the
    :class:`SessionDetail`.
    """

    resource = fields.StringField(required=True)
    """The modeling imaging store resource name, e.g. ``pk_R3y9``."""

    result = fields.DictField(
        field=mongoengine.EmbeddedDocumentField(ParameterResult)
    )
    """
    The modeling {*parameter*: *result*} dictionary, where:

    - *parameter* is the lower-case underscore parameter key, e.g.
      ``k_trans``.

    - *result* is the corresponding :class:`ParameterResult`

    The parameters are determined by the :class:`Protocol`
    technique. For example, the `OHSU QIN modeling workflow`_ includes
    the following outputs for the FXL (`Tofts standard`_) model and the
    FXR (`shutter speed`_) model:

    - *fxl_k_trans*, *fxr_k_trans*: the |Ktrans| vascular permeability
       transfer constant

    - *delta_k_trans*: the FXR-FXL |Ktrans| difference

    - *fxl_v_e*, *fxr_v_e*: the |ve| extravascular extracellular volume
       fraction

    - *fxr_tau_i*: the |taui| intracellular |H2O| mean lifetime

    - *fxl_chi_sq*, *fxr_chi_sq*: the |chisq| intensity goodness of fit

    The REST client is responsible for anticipating and interpreting the
    meaning of the *parameter* based on the modeling technique. For
    example, if the image store has a session modeling resource
    ``pk_h7Jtl`` which includes the following files::

        k_trans.nii.gz
        k_trans_overlay.nii.gz
        chi_sq.nii.gz
        chi_sq_overlay.nii.gz

    then a REST database update client might calculate the average |Ktrans|
    and |chisq| values and populate the REST database as follows::

        from qirest_client.helpers import database
        // The scan protocol.
        t1 = database.get_or_create(Protocol, dict(scan_type='T1'))
        // The modeling protocol.
        tofts = database.get_or_create(Protocol,
                                       dict(technique='Tofts'))
        // The modeling results.
        ktrans_label_map = LabelMap(filename='k_trans_overlay.nii.gz',
                                    color_table='jet.txt')
        ktrans = Modeling.ParameterResult(name='k_trans.nii.gz',
                                          average=k_trans_avg,
                                          label_map=ktrans_label_map)
        chisq_label_map = LabelMap(filename='k_trans_overlay.nii.gz',
                                   color_table='jet.txt')
        chisq = Modeling.ParameterResult(name='chi_sq.nii.gz',
                                         average=chi_sq_avg,
                                         label_map=chisq_label_map)
        result = dict(ktrans=ktrans, chisq=chisq)
        // The modeling object.
        session.modeling = Modeling(protocol=tofts, source=t1,
                                    resource='pk_h7Jtl', result=result)

    It is then the responsibility of an imaging web app REST read client
    to interpret the modeling result dictionary items and display them
    appropriately.

    .. reST substitutions:
    .. include:: <isogrk3.txt>
    .. |H2O| replace:: H\ :sub:`2`\ O
    .. |Ktrans| replace:: K\ :sup:`trans`
    .. |ve| replace:: v\ :sub:`e`
    .. |taui| replace:: |tau|\ :sub:`i`
    .. |chisq| replace:: |chi|\ :sup:`2`

    .. _OHSU QIN modeling workflow: http://qipipe.readthedocs.org/en/latest/api/pipeline.html#modeling
    .. _Tofts standard: http://onlinelibrary.wiley.com/doi/10.1002/(SICI)1522-2586(199909)10:3%3C223::AID-JMRI2%3E3.0.CO;2-S/abstract
    .. _shutter speed: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2582583
    """

    def __str__(self):
        return "Modeling %s" % self.resource


class SessionDetail(mongoengine.Document):
    """The MR session detailed content."""

    meta = dict(collection='qiprofile_session_detail')

    scans = fields.ListField(field=mongoengine.EmbeddedDocumentField(Scan))
    """The list of scans."""


class Session(Encounter):
    """The MR session (a.k.a. *study* in DICOM terminology)."""

    modelings = fields.ListField(
        field=fields.EmbeddedDocumentField(Modeling)
    )
    """The modeling performed on the session."""

    tumor_extents = fields.ListField(
        field=fields.EmbeddedDocumentField(TumorExtent)
    )
    """The tumor extents measured from the scan."""

    preview = fields.EmbeddedDocumentField(SingleImageResource)
    """
    The scan graphical display preview image resource object.
    The preview is a a Session resource rather than a Scan
    resource so that the client does not need to load the
    SessionDetail in order to access the preview image.
    """

    acquisition_parameters = fields.DictField;
    """
    The image acquisition parameters dictionary.
    The dictionary includes DICOM metadata that is common to
    all of the captured scan images.
    """

    detail = fields.ReferenceField(SessionDetail)
    """The session detail reference."""

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        """Cascade delete this Session's detail."""

        if self.detail:
            self.detail.delete()

signals.pre_delete.connect(Session.pre_delete, sender=Session)
