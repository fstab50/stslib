# stsAval v0.3.6 | Release Notes

* * *
**Release date**:  October 22, 2017
* * *

## Features Implemented in v0.3.6

* **STSToken Format**: stsAval now generates session tokens in a custom format which is much  
easier to consume.  See [FAQ](../FAQ.md) documentation.

* **STSToken Format**: stsAval now generates session tokens in a custom format which is much  
easier to consume.  See [FAQ](../FAQ.md) documentation.

* **Dual Credential Format Support**:   Credentials may be generated in one of 2 formats:
    1. 'stsAval' Custom Format (default).  See [FAQ](../FAQ.md) documentation.
    2. `boto` Format:  native format generated by Amazon's boto library

* **Logging Formats**:  stsAval now has 2 log output formats available:
    * Filehandler
    * Streamhandler

    Either can be set as the default in the `~/.stsAval/config.yml` module

    Log format can be set at runtime via the `log_mode` parameter provided when `StsCore` instantiated

* **Documentation Updates**:  README received extensive updates in this release

* Various bug fixes

* * *

## Limitations

#### Generation of Multiple Credential Sets

Credential sets which are maintained simultaneously is planned for v2.0


* * *

( [Back to README](../README.md) )


* * *