# v1.6.4 (Sat Oct 28 2023)

#### 🏠 Internal

- Fix build - remove setuptools-git-versioning from pyproject.toml and also versioneer.py from MANIFEST [#94](https://github.com/Lykos153/AnnexRemote/pull/94) ([@yarikoptic](https://github.com/yarikoptic))

#### Authors: 1

- Yaroslav Halchenko ([@yarikoptic](https://github.com/yarikoptic))

---

# v1.6.3 (Fri Oct 27 2023)

#### 🐛 Bug Fix

- Add actual twine upload call to .autorc to fix release to make it appear on PyPI [#91](https://github.com/Lykos153/AnnexRemote/pull/91) ([@yarikoptic](https://github.com/yarikoptic))

#### 🏠 Internal

- Revert "Add "workflow_dispatch:" as a way to trigger workflow" [#92](https://github.com/Lykos153/AnnexRemote/pull/92) ([@yarikoptic](https://github.com/yarikoptic))
- Add "workflow_dispatch:" as a way to trigger workflow [#92](https://github.com/Lykos153/AnnexRemote/pull/92) ([@yarikoptic](https://github.com/yarikoptic))

#### Authors: 1

- Yaroslav Halchenko ([@yarikoptic](https://github.com/yarikoptic))

---

# v1.6.1 (Thu Oct 26 2023)

#### 🐛 Bug Fix

- Fix invalid escape sequences in test regexes [#76](https://github.com/Lykos153/AnnexRemote/pull/76) ([@musicinmybrain](https://github.com/musicinmybrain))
- Add 3.10 and 3.11 into the mix of supported Pythons [#62](https://github.com/Lykos153/AnnexRemote/pull/62) ([@yarikoptic](https://github.com/yarikoptic))
- Migrate from setup.py to pyproject.toml [#51](https://github.com/Lykos153/AnnexRemote/pull/51) ([@Lykos153](https://github.com/Lykos153))

#### ⚠️ Pushed to `master`

- Remove support for Python 3.6 (EOL) ([@Lykos153](https://github.com/Lykos153))

#### 🏠 Internal

- Use released 3.12 not rc on github workflows [#89](https://github.com/Lykos153/AnnexRemote/pull/89) ([@yarikoptic](https://github.com/yarikoptic))
- chore(deps): update pre-commit hook psf/black to v23.10.1 [#87](https://github.com/Lykos153/AnnexRemote/pull/87) ([@renovate[bot]](https://github.com/renovate[bot]))
- Codespell fix some typos [#86](https://github.com/Lykos153/AnnexRemote/pull/86) ([@yarikoptic](https://github.com/yarikoptic))
- chore(deps): update pre-commit hook psf/black to v23.10.0 [#84](https://github.com/Lykos153/AnnexRemote/pull/84) ([@renovate[bot]](https://github.com/renovate[bot]))
- Use intuit auto for release [#73](https://github.com/Lykos153/AnnexRemote/pull/73) ([@yarikoptic](https://github.com/yarikoptic))
- chore(deps): update actions/checkout action to v4 [#79](https://github.com/Lykos153/AnnexRemote/pull/79) ([@renovate[bot]](https://github.com/renovate[bot]))
- chore(deps): update pre-commit hook psf/black to v23.9.1 [#77](https://github.com/Lykos153/AnnexRemote/pull/77) ([@renovate[bot]](https://github.com/renovate[bot]))
- chore(deps): update codespell-project/actions-codespell action to v2 [#74](https://github.com/Lykos153/AnnexRemote/pull/74) ([@renovate[bot]](https://github.com/renovate[bot]))
- chore(deps): update pre-commit hook psf/black to v23.3.0 [#70](https://github.com/Lykos153/AnnexRemote/pull/70) ([@renovate[bot]](https://github.com/renovate[bot]))
- chore(deps): update pre-commit hook psf/black to v23 [#68](https://github.com/Lykos153/AnnexRemote/pull/68) ([@renovate[bot]](https://github.com/renovate[bot]))
- chore(deps): update actions/checkout action to v3 [#58](https://github.com/Lykos153/AnnexRemote/pull/58) ([@renovate[bot]](https://github.com/renovate[bot]))
- Add codespell CI, fix typos with 1 of its runs with -w [#63](https://github.com/Lykos153/AnnexRemote/pull/63) ([@yarikoptic](https://github.com/yarikoptic))
- Update pre-commit hook psf/black to v22.8.0 [#57](https://github.com/Lykos153/AnnexRemote/pull/57) ([@renovate[bot]](https://github.com/renovate[bot]))
- Update pre-commit hook psf/black to v22.6.0 [#56](https://github.com/Lykos153/AnnexRemote/pull/56) ([@renovate[bot]](https://github.com/renovate[bot]))
- renovate: Add pre-commit [#55](https://github.com/Lykos153/AnnexRemote/pull/55) ([@Lykos153](https://github.com/Lykos153))
- Update actions/setup-python action to v4 [#50](https://github.com/Lykos153/AnnexRemote/pull/50) ([@renovate[bot]](https://github.com/renovate[bot]))
- Configure pre-commit for nosetests [#54](https://github.com/Lykos153/AnnexRemote/pull/54) ([@Lykos153](https://github.com/Lykos153))
- Use black [#53](https://github.com/Lykos153/AnnexRemote/pull/53) ([@Lykos153](https://github.com/Lykos153))
- Update Versioneer to 0.22 [#49](https://github.com/Lykos153/AnnexRemote/pull/49) ([@hugovk](https://github.com/hugovk) [@Lykos153](https://github.com/Lykos153))
- Use versions instead of commit hashes for actions [#48](https://github.com/Lykos153/AnnexRemote/pull/48) ([@Lykos153](https://github.com/Lykos153))
- Update actions/checkout action to v3 [#43](https://github.com/Lykos153/AnnexRemote/pull/43) ([@renovate-bot](https://github.com/renovate-bot))
- Update actions/setup-python action to v3 [#44](https://github.com/Lykos153/AnnexRemote/pull/44) ([@renovate-bot](https://github.com/renovate-bot))
- Update pypa/gh-action-pypi-publish digest to 717ba43 [#41](https://github.com/Lykos153/AnnexRemote/pull/41) ([@renovate-bot](https://github.com/renovate-bot))
- Configure Renovate [#39](https://github.com/Lykos153/AnnexRemote/pull/39) ([@renovate-bot](https://github.com/renovate-bot) [@renovate[bot]](https://github.com/renovate[bot]))
- Create action to publish on pypi [#35](https://github.com/Lykos153/AnnexRemote/pull/35) ([@Lykos153](https://github.com/Lykos153))

#### 📝 Documentation

- Include v1.6.1 produced CHANGELOG (failed to push/finalize the release) [#81](https://github.com/Lykos153/AnnexRemote/pull/81) (auto@nil [@yarikoptic](https://github.com/yarikoptic))
- Remove bold claim that is not true anymore [#72](https://github.com/Lykos153/AnnexRemote/pull/72) ([@Lykos153](https://github.com/Lykos153))
- Annotated code snippets in README as python for proper coloring etc [#64](https://github.com/Lykos153/AnnexRemote/pull/64) ([@yarikoptic](https://github.com/yarikoptic))
- renovate: ignore docs/** [#47](https://github.com/Lykos153/AnnexRemote/pull/47) ([@Lykos153](https://github.com/Lykos153))
- Add test and pypi badge to readme [#38](https://github.com/Lykos153/AnnexRemote/pull/38) ([@Lykos153](https://github.com/Lykos153))

#### 🧪 Tests

- Use pytest-cov and upload coverage to codecov [#82](https://github.com/Lykos153/AnnexRemote/pull/82) ([@yarikoptic](https://github.com/yarikoptic))
- Switch from nose to pytest, add 3.12.0-rc3 into matrix [#80](https://github.com/Lykos153/AnnexRemote/pull/80) ([@yarikoptic](https://github.com/yarikoptic))
- Add github action for running nosetests [#37](https://github.com/Lykos153/AnnexRemote/pull/37) ([@Lykos153](https://github.com/Lykos153))

#### Authors: 7

- [@renovate[bot]](https://github.com/renovate[bot])
- auto (auto@nil)
- Ben Beasley ([@musicinmybrain](https://github.com/musicinmybrain))
- Hugo van Kemenade ([@hugovk](https://github.com/hugovk))
- Mend Renovate ([@renovate-bot](https://github.com/renovate-bot))
- Silvio Ankermann ([@Lykos153](https://github.com/Lykos153))
- Yaroslav Halchenko ([@yarikoptic](https://github.com/yarikoptic))

---

# v1.6.1 (Mon Sep 25 2023)

#### 🐛 Bug Fix

- Fix invalid escape sequences in test regexes [#76](https://github.com/Lykos153/AnnexRemote/pull/76) ([@musicinmybrain](https://github.com/musicinmybrain))
- Add 3.10 and 3.11 into the mix of supported Pythons [#62](https://github.com/Lykos153/AnnexRemote/pull/62) ([@yarikoptic](https://github.com/yarikoptic))
- Migrate from setup.py to pyproject.toml [#51](https://github.com/Lykos153/AnnexRemote/pull/51) ([@Lykos153](https://github.com/Lykos153))

#### ⚠️ Pushed to `master`

- Remove support for Python 3.6 (EOL) ([@Lykos153](https://github.com/Lykos153))

#### 🏠 Internal

- Use intuit auto for release [#73](https://github.com/Lykos153/AnnexRemote/pull/73) ([@yarikoptic](https://github.com/yarikoptic))
- chore(deps): update actions/checkout action to v4 [#79](https://github.com/Lykos153/AnnexRemote/pull/79) ([@renovate[bot]](https://github.com/renovate[bot]))
- chore(deps): update pre-commit hook psf/black to v23.9.1 [#77](https://github.com/Lykos153/AnnexRemote/pull/77) ([@renovate[bot]](https://github.com/renovate[bot]))
- chore(deps): update codespell-project/actions-codespell action to v2 [#74](https://github.com/Lykos153/AnnexRemote/pull/74) ([@renovate[bot]](https://github.com/renovate[bot]))
- chore(deps): update pre-commit hook psf/black to v23.3.0 [#70](https://github.com/Lykos153/AnnexRemote/pull/70) ([@renovate[bot]](https://github.com/renovate[bot]))
- chore(deps): update pre-commit hook psf/black to v23 [#68](https://github.com/Lykos153/AnnexRemote/pull/68) ([@renovate[bot]](https://github.com/renovate[bot]))
- chore(deps): update actions/checkout action to v3 [#58](https://github.com/Lykos153/AnnexRemote/pull/58) ([@renovate[bot]](https://github.com/renovate[bot]))
- Add codespell CI, fix typos with 1 of its runs with -w [#63](https://github.com/Lykos153/AnnexRemote/pull/63) ([@yarikoptic](https://github.com/yarikoptic))
- Update pre-commit hook psf/black to v22.8.0 [#57](https://github.com/Lykos153/AnnexRemote/pull/57) ([@renovate[bot]](https://github.com/renovate[bot]))
- Update pre-commit hook psf/black to v22.6.0 [#56](https://github.com/Lykos153/AnnexRemote/pull/56) ([@renovate[bot]](https://github.com/renovate[bot]))
- renovate: Add pre-commit [#55](https://github.com/Lykos153/AnnexRemote/pull/55) ([@Lykos153](https://github.com/Lykos153))
- Update actions/setup-python action to v4 [#50](https://github.com/Lykos153/AnnexRemote/pull/50) ([@renovate[bot]](https://github.com/renovate[bot]))
- Configure pre-commit for nosetests [#54](https://github.com/Lykos153/AnnexRemote/pull/54) ([@Lykos153](https://github.com/Lykos153))
- Use black [#53](https://github.com/Lykos153/AnnexRemote/pull/53) ([@Lykos153](https://github.com/Lykos153))
- Update Versioneer to 0.22 [#49](https://github.com/Lykos153/AnnexRemote/pull/49) ([@hugovk](https://github.com/hugovk) [@Lykos153](https://github.com/Lykos153))
- Use versions instead of commit hashes for actions [#48](https://github.com/Lykos153/AnnexRemote/pull/48) ([@Lykos153](https://github.com/Lykos153))
- Update actions/checkout action to v3 [#43](https://github.com/Lykos153/AnnexRemote/pull/43) ([@renovate-bot](https://github.com/renovate-bot))
- Update actions/setup-python action to v3 [#44](https://github.com/Lykos153/AnnexRemote/pull/44) ([@renovate-bot](https://github.com/renovate-bot))
- Update pypa/gh-action-pypi-publish digest to 717ba43 [#41](https://github.com/Lykos153/AnnexRemote/pull/41) ([@renovate-bot](https://github.com/renovate-bot))
- Configure Renovate [#39](https://github.com/Lykos153/AnnexRemote/pull/39) ([@renovate-bot](https://github.com/renovate-bot) [@renovate[bot]](https://github.com/renovate[bot]))
- Create action to publish on pypi [#35](https://github.com/Lykos153/AnnexRemote/pull/35) ([@Lykos153](https://github.com/Lykos153))

#### 📝 Documentation

- Remove bold claim that is not true anymore [#72](https://github.com/Lykos153/AnnexRemote/pull/72) ([@Lykos153](https://github.com/Lykos153))
- Annotated code snippets in README as python for proper coloring etc [#64](https://github.com/Lykos153/AnnexRemote/pull/64) ([@yarikoptic](https://github.com/yarikoptic))
- renovate: ignore docs/** [#47](https://github.com/Lykos153/AnnexRemote/pull/47) ([@Lykos153](https://github.com/Lykos153))
- Add test and pypi badge to readme [#38](https://github.com/Lykos153/AnnexRemote/pull/38) ([@Lykos153](https://github.com/Lykos153))

#### 🧪 Tests

- Switch from nose to pytest, add 3.12.0-rc3 into matrix [#80](https://github.com/Lykos153/AnnexRemote/pull/80) ([@yarikoptic](https://github.com/yarikoptic))
- Add github action for running nosetests [#37](https://github.com/Lykos153/AnnexRemote/pull/37) ([@Lykos153](https://github.com/Lykos153))

#### Authors: 6

- [@renovate[bot]](https://github.com/renovate[bot])
- Ben Beasley ([@musicinmybrain](https://github.com/musicinmybrain))
- Hugo van Kemenade ([@hugovk](https://github.com/hugovk))
- Mend Renovate ([@renovate-bot](https://github.com/renovate-bot))
- Silvio Ankermann ([@Lykos153](https://github.com/Lykos153))
- Yaroslav Halchenko ([@yarikoptic](https://github.com/yarikoptic))

---

# 1.6.0 (2021-10-11)

#### Added

* Logging handler
* CHANGELOG.md

#### Removed

* Support for Python 2.7
