# Rubin Observatory Sample Alerts

The Vera C. Rubin Observatory is releasing sample alert packets produced by its pipelines run on precursor survey data.
These alerts are intended to provide candidate community alert brokers as well as science users the chance to preview the alert format and contents and to provide feedback to the project.

## Obtaining the Data

Sample alert data may be obtained at [this link](https://lsst.ncsa.illinois.edu/~ebellm/sample_precursor_alerts/).
We anticipate providing reprocessed and updated alert samples as pipeline development progresses, so the data are arranged in a directory structure:

```
    sample_precursor_alerts/
	YYYY-MM-DD/
	    dataset/
		all_visits_{dataset}_{date}.avro
		association_{dataset}_{date}.db
		single_ccd_sample_{dataset}_{date}.avro
		single_visit_sample_{dataset}_{date}.avro
```

### Alert packets

Alerts are provided as Snappy-compressed [Avro](https://avro.apache.org/) files.
The schema used to store the alerts is included in the file.

As the complete sample is about 1 TB, we include two smaller subsets—alerts from a single CCD-visit, and all of the alerts from all CCDs in a single visit.

### Database

In addition to accessing alert packets via community brokers and through the project-provided Alert Filtering Service, during the survey members of the data rights community will be able to query the relational Prompt Products Database (PPDB).
The contents of the alerts are correspond directly to the PPDB `DIASource`, `DIAForcedSource`, `DIAObject`, and `SSObject` records.
For some use cases direct queries to the PPDB may be more efficient than processing alert packets.

To allow users to explore these different modes of data access, we are also providing the PPDB (`association_{dataset}_{date}.db`) from which the sample alerts were generated as an [SQLite](https://www.sqlite.org) database.
The SQLite database can be queried using SQL through a variety of interfaces.

Note that in operations, users will query the PPDB using [ADQL](http://www.ivoa.net/documents/ADQL/) via a [TAP service](http://www.ivoa.net/documents/TAP/).

### Software

Users should install [lsst.alert.packet](https://github.com/lsst/alert_packet) to parse alerts and optionally [alert-stream-simulator](https://github.com/lsst-dm/alert-stream-simulator/) and [alert-stream](https://github.com/lsst-dm/alert_stream) if they wish to simulate a Kafka alert stream.

## External References and Additional Resources

The [Data Products Definition Document (DPDD)](http://ls.st/dpdd) provides a change-controlled guide to what scientific contents are planned for alerts and other Rubin Observatory data products.

[LDM-612](http://ls.st/LDM-612) describes "Plans and Policies for LSST Alert Distribution," including a high-level overview of the relevant components, a summary of data rights issues, and extensive discussion of the role and selection of community alert brokers.

[DMTN-093](https://dmtn-093.lsst.io/) presents the technical design of the alert distribution system.

[DMTN-102](https://dmtn-102.lsst.io/) summarizes "Key Numbers" for alerts, estimating numbers, sizing, etc.

[lsst.alert.packet](https://github.com/lsst/alert_packet) is a Python package that contains alert schemas as well as utilities for reading and writing Rubin alert packets.

Community broker authors will be interested in simulating the Kafka alert stream itself.  
[alert-stream-simulator](https://github.com/lsst-dm/alert-stream-simulator/) provides the relevant code; the overall design is discussed in [DMTN-149](https://dmtn-149.lsst.io/).
[alert_stream](https://github.com/lsst-dm/alert_stream) currently contains additional code for converting from the [Confluent Wire Format](https://dmtn-093.lsst.io/#management-and-evolution) used in the Kafka stream.

## Data Sources

### DECam-HiTS

Sample alerts are provided from a subset of the DECam High Cadence Transient Search (HiTS; [Förster et al. 2016](https://ui.adsabs.harvard.edu/abs/2016ApJ...832..155F/abstract)).

We process g-band data from three fields (`Blind15A_26`, `Blind15A_40`, and `Blind15A_42`) from the 2015 campaign and use coadded templates built from the matching fields in the 2014 campaign. In total there are 5020 processed CCD-visits.

Users interested in performing their own reductions can obtain these data [here](https://github.com/lsst/ap_verify_hits2015).
The `ap_verify` package in the LSST Stack can be used to [process this dataset](https://pipelines.lsst.io/modules/lsst.ap.verify/running.html).

## Limitations and Caveats (2020-07-06)

The Alert Production pipelines are not yet complete, so not all of the alert contents prescribed by the DPDD are populated in these sample alerts.
Missing fields and quantities that failed to fit or process will have `null` entries.
We describe the most significant omissions below.

### Sample

Each `DIASource` detected at or above 5 sigma in the difference image produces a `DIASource` entry in the PPDB and a corresponding alert packet.
Because detection SNR is different than the measured SNR of a point-source fit, not all `DIASources` will have `psFlux/psFluxErr > 5`.

The sample is not filtered for artifacts or bad subtractions.
Through visual inspection we suggest that the current proportion of artifacts to real transients is about 4:1.
We expect continued improvement in this ratio.

### Formats

The Avro format, schema structure, and alert contents released here reflect the current baseline, but users should be prepared for continued evolution and potentially breaking changes.

The top-level `AlertID` record is currently populated with the triggering `diaSourceId`, but we plan to migrate to a unique id in the future.

### `DIASource` Records

* The detection signal-to-noise (`SNR`) is not populated 
* Trailed source fits are not implemented
* No extendedness or spuriousness score is included
	
### `DIAObject` Records

* Parallax and proper motion fitting is not performed
* Timeseries features are not included
* There are no associations to Data Release Objects

### `SSObject` Records

Attribution of known Solar System objects is not yet implemented, so while observations of asteroids are present among the sample alerts they are not yet labelled as `SSObjects`.

### `DIAForcedSource` Records

For some DIAObjects, the centroid is inaccurate due to image subtraction failures (e.g., for bright stars). 
For these sources the forced PSF fluxes will be highly biased.

### Upper Limits

When forced photometry measurements do not exist, we will provide historical noise estimates to allow determination of coarse upper limits.
This data is not yet included in the sample alerts.

### Cutouts

We convert image cutouts to [`astropy.cddata.CCDData`](https://docs.astropy.org/en/stable/api/astropy.nddata.CCDData.html) objects and then provide FITS serializations in the alert packet. 

At present, `CCDData` does not include a PSF representation, as required for Rubin alerts.
We expect to propose such a representation and include it in future releases of sample alerts.

`CCDData` also does not currently support `xy0`, which would allow cutouts to have the same pixel coordinates as they do in the full CCD exposure.

Some detections on bleed trails or other artifacts generate extremely large footprints and correspondingly large cutouts.
We expect to mitigate this problem in the future.

## Feedback

We welcome questions, comments, and suggestions about these sample alerts via the community.lsst.org [Data Q&A Forum](https://community.lsst.org/c/sci/data/34).

