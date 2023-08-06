Change Log
==========

`Unreleased <https://github.com/zalando/expan/tree/HEAD>`__
-----------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.4.5...HEAD>`__

**Implemented enhancements:**

-  Bad code duplication in experiment.py
   `#81 <https://github.com/zalando/expan/issues/81>`__
-  pip == 8.1.0 requirement
   `#76 <https://github.com/zalando/expan/issues/76>`__

**Fixed bugs:**

-  Experiment.sga() assumes features and KPIs are merged in self.metrics
   `#87 <https://github.com/zalando/expan/issues/87>`__
-  pctile can be undefined in ``Results.to\_json\(\)``
   `#78 <https://github.com/zalando/expan/issues/78>`__

**Closed issues:**

-  Results.to\_json() => TypeError: Object of type 'UserWarning' is not
   JSON serializable
   `#77 <https://github.com/zalando/expan/issues/77>`__
-  Rethink Results structure
   `#66 <https://github.com/zalando/expan/issues/66>`__

**Merged pull requests:**

-  new dataframe tree traverser in to\_json()
   `#92 <https://github.com/zalando/expan/pull/92>`__
   (`gbordyugov <https://github.com/gbordyugov>`__)
-  updated requirements.txt to have 'greater than' dependencies instead
   … `#89 <https://github.com/zalando/expan/pull/89>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  pip version requirement
   `#88 <https://github.com/zalando/expan/pull/88>`__
   (`gbordyugov <https://github.com/gbordyugov>`__)
-  Test `#86 <https://github.com/zalando/expan/pull/86>`__
   (`s4826 <https://github.com/s4826>`__)
-  merging in categorical binning
   `#84 <https://github.com/zalando/expan/pull/84>`__
   (`gbordyugov <https://github.com/gbordyugov>`__)
-  Add documentation of the weighting logic
   `#83 <https://github.com/zalando/expan/pull/83>`__
   (`jbao <https://github.com/jbao>`__)
-  Early stopping `#80 <https://github.com/zalando/expan/pull/80>`__
   (`jbao <https://github.com/jbao>`__)
-  a couple of minor cleanups
   `#79 <https://github.com/zalando/expan/pull/79>`__
   (`gbordyugov <https://github.com/gbordyugov>`__)
-  Merge to\_json() changes
   `#75 <https://github.com/zalando/expan/pull/75>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  Feature/early stopping
   `#73 <https://github.com/zalando/expan/pull/73>`__
   (`jbao <https://github.com/jbao>`__)

`v0.4.5 <https://github.com/zalando/expan/tree/v0.4.5>`__ (2017-02-10)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.4.4...v0.4.5>`__

**Fixed bugs:**

-  Numbers cannot appear in variable names for derived metrics
   `#58 <https://github.com/zalando/expan/issues/58>`__

**Merged pull requests:**

-  Feature/results and to json refactor
   `#74 <https://github.com/zalando/expan/pull/74>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  Merge to\_json() and prob\_uplift\_over\_zero changes
   `#72 <https://github.com/zalando/expan/pull/72>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  regex fix, see https://github.com/zalando/expan/issues/58
   `#70 <https://github.com/zalando/expan/pull/70>`__
   (`gbordyugov <https://github.com/gbordyugov>`__)

`v0.4.4 <https://github.com/zalando/expan/tree/v0.4.4>`__ (2017-02-09)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.4.3...v0.4.4>`__

**Implemented enhancements:**

-  Add argument assume\_normal and treatment\_cost to
   calculate\_prob\_uplift\_over\_zero() and
   prob\_uplift\_over\_zero\_single\_metric()
   `#26 <https://github.com/zalando/expan/issues/26>`__
-  host intro slides (from the ipython notebook) somewhere for public
   viewing `#10 <https://github.com/zalando/expan/issues/10>`__

**Closed issues:**

-  migrate issues from github enterprise
   `#20 <https://github.com/zalando/expan/issues/20>`__

**Merged pull requests:**

-  Feature/results and to json refactor
   `#71 <https://github.com/zalando/expan/pull/71>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  new to\_json() functionality and improved vim support
   `#67 <https://github.com/zalando/expan/pull/67>`__
   (`mkolarek <https://github.com/mkolarek>`__)

`v0.4.3 <https://github.com/zalando/expan/tree/v0.4.3>`__ (2017-02-07)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.4.2...v0.4.3>`__

**Closed issues:**

-  coverage % is misleading
   `#23 <https://github.com/zalando/expan/issues/23>`__

**Merged pull requests:**

-  Vim modelines `#63 <https://github.com/zalando/expan/pull/63>`__
   (`gbordyugov <https://github.com/gbordyugov>`__)
-  Feature/octo 1253 expan results in json
   `#62 <https://github.com/zalando/expan/pull/62>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  0.4.2 release `#60 <https://github.com/zalando/expan/pull/60>`__
   (`mkolarek <https://github.com/mkolarek>`__)

`v0.4.2 <https://github.com/zalando/expan/tree/v0.4.2>`__ (2016-12-08)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.4.1...v0.4.2>`__

**Fixed bugs:**

-  frequency table in the chi square test doesn't respect the order of
   categories `#56 <https://github.com/zalando/expan/issues/56>`__

**Merged pull requests:**

-  OCTO-1143 Review outlier filtering
   `#59 <https://github.com/zalando/expan/pull/59>`__
   (`domheger <https://github.com/domheger>`__)
-  Workaround to fix #56
   `#57 <https://github.com/zalando/expan/pull/57>`__
   (`jbao <https://github.com/jbao>`__)

`v0.4.1 <https://github.com/zalando/expan/tree/v0.4.1>`__ (2016-10-18)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.4.0...v0.4.1>`__

**Merged pull requests:**

-  small doc cleanup `#55 <https://github.com/zalando/expan/pull/55>`__
   (`jbao <https://github.com/jbao>`__)
-  Add comments to cli.py
   `#54 <https://github.com/zalando/expan/pull/54>`__
   (`igusher <https://github.com/igusher>`__)
-  Feature/octo 545 add consolidate documentation
   `#53 <https://github.com/zalando/expan/pull/53>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  added os.path.join instead of manual string concatenations with '/'
   `#52 <https://github.com/zalando/expan/pull/52>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  Feature/octo 958 outlier filtering
   `#50 <https://github.com/zalando/expan/pull/50>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  Sort KPIs in reverse order before matching them in the formula
   `#49 <https://github.com/zalando/expan/pull/49>`__
   (`jbao <https://github.com/jbao>`__)

`v0.4.0 <https://github.com/zalando/expan/tree/v0.4.0>`__ (2016-08-19)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.3.4...v0.4.0>`__

**Closed issues:**

-  Support 'overall ratio' metrics (e.g. conversion rate/return rate) as
   opposed to per-entity ratios
   `#44 <https://github.com/zalando/expan/issues/44>`__

**Merged pull requests:**

-  merging dev to master
   `#48 <https://github.com/zalando/expan/pull/48>`__
   (`jbao <https://github.com/jbao>`__)
-  OCTO-825 overall metric
   `#47 <https://github.com/zalando/expan/pull/47>`__
   (`jbao <https://github.com/jbao>`__)
-  Bump version: 0.3.2 → 0.3.4
   `#46 <https://github.com/zalando/expan/pull/46>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  Bug/fix dependencies
   `#45 <https://github.com/zalando/expan/pull/45>`__
   (`mkolarek <https://github.com/mkolarek>`__)

`v0.3.4 <https://github.com/zalando/expan/tree/v0.3.4>`__ (2016-08-08)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.3.3...v0.3.4>`__

**Closed issues:**

-  perform trend analysis cumulatively
   `#31 <https://github.com/zalando/expan/issues/31>`__
-  Python3 `#21 <https://github.com/zalando/expan/issues/21>`__

**Merged pull requests:**

-  Feature/2to3 `#43 <https://github.com/zalando/expan/pull/43>`__
   (`mkolarek <https://github.com/mkolarek>`__)

`v0.3.3 <https://github.com/zalando/expan/tree/v0.3.3>`__ (2016-08-02)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.3.2...v0.3.3>`__

**Merged pull requests:**

-  Merge pull request #41 from zalando/master
   `#42 <https://github.com/zalando/expan/pull/42>`__
   (`jbao <https://github.com/jbao>`__)
-  master to dev `#41 <https://github.com/zalando/expan/pull/41>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  Bump version: 0.3.1 → 0.3.2
   `#40 <https://github.com/zalando/expan/pull/40>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  Revert "Merge pull request #35 from zalando/dev"
   `#39 <https://github.com/zalando/expan/pull/39>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  Merge pull request #35 from zalando/dev
   `#38 <https://github.com/zalando/expan/pull/38>`__
   (`mkolarek <https://github.com/mkolarek>`__)

`v0.3.2 <https://github.com/zalando/expan/tree/v0.3.2>`__ (2016-08-02)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.3.1...v0.3.2>`__

**Merged pull requests:**

-  Bugfix/trend analysis bin label
   `#37 <https://github.com/zalando/expan/pull/37>`__
   (`jbao <https://github.com/jbao>`__)
-  Added cumulative trends analysis OCTO-814
   `#36 <https://github.com/zalando/expan/pull/36>`__
   (`domheger <https://github.com/domheger>`__)
-  Merging 0.3.1 to master
   `#35 <https://github.com/zalando/expan/pull/35>`__
   (`domheger <https://github.com/domheger>`__)

`v0.3.1 <https://github.com/zalando/expan/tree/v0.3.1>`__ (2016-07-15)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.3.0...v0.3.1>`__

**Merged pull requests:**

-  Bugfix/prob uplift over 0
   `#34 <https://github.com/zalando/expan/pull/34>`__
   (`jbao <https://github.com/jbao>`__)
-  Master `#30 <https://github.com/zalando/expan/pull/30>`__
   (`mkolarek <https://github.com/mkolarek>`__)

`v0.3.0 <https://github.com/zalando/expan/tree/v0.3.0>`__ (2016-06-23)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.2.5...v0.3.0>`__

**Implemented enhancements:**

-  Add P(uplift>0) as a statistic
   `#2 <https://github.com/zalando/expan/issues/2>`__
-  Added function to calculate P(uplift>0)
   `#24 <https://github.com/zalando/expan/pull/24>`__
   (`jbao <https://github.com/jbao>`__)

**Merged pull requests:**

-  updated travis.yml `#29 <https://github.com/zalando/expan/pull/29>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  Master `#28 <https://github.com/zalando/expan/pull/28>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  Master `#27 <https://github.com/zalando/expan/pull/27>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  only store the p-value in the chi-square test result object
   `#22 <https://github.com/zalando/expan/pull/22>`__
   (`jbao <https://github.com/jbao>`__)

`v0.2.5 <https://github.com/zalando/expan/tree/v0.2.5>`__ (2016-05-30)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.2.4...v0.2.5>`__

**Implemented enhancements:**

-  Implement \_\_version\_\_
   `#14 <https://github.com/zalando/expan/issues/14>`__

**Closed issues:**

-  upload full documentation!
   `#1 <https://github.com/zalando/expan/issues/1>`__

**Merged pull requests:**

-  implement expan.\_\_version\_\_
   `#19 <https://github.com/zalando/expan/pull/19>`__
   (`pangeran-bottor <https://github.com/pangeran-bottor>`__)
-  Mainly documentation changes, as well as travis config updates
   `#17 <https://github.com/zalando/expan/pull/17>`__
   (`robertmuil <https://github.com/robertmuil>`__)
-  Update README.rst `#16 <https://github.com/zalando/expan/pull/16>`__
   (`pangeran-bottor <https://github.com/pangeran-bottor>`__)
-  added cli module `#11 <https://github.com/zalando/expan/pull/11>`__
   (`mkolarek <https://github.com/mkolarek>`__)
-  new travis config specifying that only master and dev should be built
   `#4 <https://github.com/zalando/expan/pull/4>`__
   (`mkolarek <https://github.com/mkolarek>`__)

`v0.2.4 <https://github.com/zalando/expan/tree/v0.2.4>`__ (2016-05-16)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.2.3...v0.2.4>`__

**Closed issues:**

-  No module named experiment and test\_data
   `#13 <https://github.com/zalando/expan/issues/13>`__

**Merged pull requests:**

-  new travis config specifying that only master and dev should be built
   `#5 <https://github.com/zalando/expan/pull/5>`__
   (`mkolarek <https://github.com/mkolarek>`__)

`v0.2.3 <https://github.com/zalando/expan/tree/v0.2.3>`__ (2016-05-06)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.2.2...v0.2.3>`__

`v0.2.2 <https://github.com/zalando/expan/tree/v0.2.2>`__ (2016-05-06)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.2.1...v0.2.2>`__

`v0.2.1 <https://github.com/zalando/expan/tree/v0.2.1>`__ (2016-05-06)
----------------------------------------------------------------------

`Full
Changelog <https://github.com/zalando/expan/compare/v0.2.0...v0.2.1>`__

`v0.2.0 <https://github.com/zalando/expan/tree/v0.2.0>`__ (2016-05-06)
----------------------------------------------------------------------

**Merged pull requests:**

-  Added detailed documentation with data formats
   `#3 <https://github.com/zalando/expan/pull/3>`__
   (`robertmuil <https://github.com/robertmuil>`__)

\* *This Change Log was automatically generated by
`github\_changelog\_generator <https://github.com/skywinder/Github-Changelog-Generator>`__*
