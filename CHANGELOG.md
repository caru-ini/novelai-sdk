# CHANGELOG

<!-- version list -->

## v0.8.0 (2026-03-28)

### Chores

- **pypi**: Replace homepage, document url to github pages
  ([`ad7f124`](https://github.com/caru-ini/novelai-sdk/commit/ad7f124d8ffd7728773b7983b734e4a95e2720c5))

### Documentation

- Remove CHANGELOG.md
  ([`d54f452`](https://github.com/caru-ini/novelai-sdk/commit/d54f4520c4ac9e9822a1092f66e51af0720b3a18))

- **for-ai**: Add anlas reverse-engineering note
  ([`09d2e20`](https://github.com/caru-ini/novelai-sdk/commit/09d2e20f9694e641fba2fb927446a58ed3f7f263))

- **readme**: Document anlas estimator
  ([`3fbb1a1`](https://github.com/caru-ini/novelai-sdk/commit/3fbb1a15bb8fa8da52e39062e672fd6d9d52affa))

- **website**: Add anlas estimator pages
  ([`a2b4c37`](https://github.com/caru-ini/novelai-sdk/commit/a2b4c37175d75413053d39e188b62b6d0666ce01))

- **website**: Add zh-hans anlas docs
  ([`6ed0563`](https://github.com/caru-ini/novelai-sdk/commit/6ed0563dc791bd3d6327f8891d8c4f4a8ec23e4a))

- **website**: Adjust sidebar ordering
  ([`6b9d29f`](https://github.com/caru-ini/novelai-sdk/commit/6b9d29fd5a79fa3b2818be5390934f9d06b2f26f))

### Features

- Add image anlas estimator
  ([`1ae740e`](https://github.com/caru-ini/novelai-sdk/commit/1ae740eb73455bdb17dde10d37a5183b1ff893f4))


## v0.7.1 (2026-02-22)

### Bug Fixes

- **python**: Restore 3.10 compatibility for typing features
  ([`36cd3f0`](https://github.com/caru-ini/novelai-sdk/commit/36cd3f056d12eb3a17422b93cc48cec5fc2c66e8))


## v0.7.0 (2026-02-22)

### Chores

- **deps**: Add rich dependency for CLI output
  ([`1a1f495`](https://github.com/caru-ini/novelai-sdk/commit/1a1f49562fb49959ac0d0aeebedd1bf59f871cf6))

### Documentation

- **readme**: Document new CLI modes and rich dependency
  ([`18a7ee4`](https://github.com/caru-ini/novelai-sdk/commit/18a7ee43d424c3acbaeb2726660c57c6163c0708))

- **website**: Add CLI quick start to getting-started guides
  ([`a690d3a`](https://github.com/caru-ini/novelai-sdk/commit/a690d3a7aaf27abd617511e43c09fa6ddbf735e0))

### Features

- **cli**: Modularize CLI and add interactive/json modes
  ([`bbae21a`](https://github.com/caru-ini/novelai-sdk/commit/bbae21a98777f4605d28727db6940299f019aae4))


## v0.6.2 (2026-02-22)

### Bug Fixes

- **image**: Check status before return for vibe encoding
  ([`8122c20`](https://github.com/caru-ini/novelai-sdk/commit/8122c202d69f66c6f565d37d6233cc22105d2cc2))


## v0.6.1 (2026-02-17)

### Bug Fixes

- **debug**: Remove debug print
  ([`707b0ba`](https://github.com/caru-ini/novelai-sdk/commit/707b0ba9ecc4c1a5d02598a39485abb1db69a3df))


## v0.6.0 (2026-02-17)

### Bug Fixes

- **converter**: Align async/sync params
  ([`24b9e7e`](https://github.com/caru-ini/novelai-sdk/commit/24b9e7e1202a41379550ffc79ed8c56e72555b8f))

### Documentation

- Update terminology to precise reference
  ([`eadc0ef`](https://github.com/caru-ini/novelai-sdk/commit/eadc0ef5cadc8efe25b217aa647003b5e64684da))

- **examples**: Add i2i and inpaint docs
  ([`143117d`](https://github.com/caru-ini/novelai-sdk/commit/143117db27166170b864de63aab6d3ffa02be230))

- **website**: Add inpaint page for i18n
  ([`8af4302`](https://github.com/caru-ini/novelai-sdk/commit/8af43027ca1a024245a9132c419906871220bb55))

- **website**: Fix typo
  ([`f178c14`](https://github.com/caru-ini/novelai-sdk/commit/f178c14b8e6d5cc8bb3892a10f5400522afee3ae))

- **website**: Update i2i page for i18n
  ([`de0b3ac`](https://github.com/caru-ini/novelai-sdk/commit/de0b3acd2727bdee00c62d7b6e5c4e232fc2481a))

### Features

- **converter**: Integrate inpainting into conversion pipeline
  ([`b58389d`](https://github.com/caru-ini/novelai-sdk/commit/b58389d6fc95f57ca1bf9157d81bd13fb7e3351f))

- **types**: Add InpaintParams and inpainting model support
  ([`8d8b891`](https://github.com/caru-ini/novelai-sdk/commit/8d8b891345c013ce93f45305bbdfcf1aaf618a50))

- **utils**: Add mask_to_base64 and resize_base64
  ([`cb42d0c`](https://github.com/caru-ini/novelai-sdk/commit/cb42d0c011b345e4eea5e448411515c59b5acff3))

### Refactoring

- **api**: Clean up Img2ImgParams and fix sigma type
  ([`1eeae06`](https://github.com/caru-ini/novelai-sdk/commit/1eeae06f96cbf878c1e3448c179804336a2ccc82))

- **example**: Remove unnecessary print
  ([`7589251`](https://github.com/caru-ini/novelai-sdk/commit/7589251c5b034c8ff15fea9585ba963fcf4837bb))


## v0.5.0 (2026-02-05)

### Documentation

- Update document for precise reference
  ([`3ae5a52`](https://github.com/caru-ini/novelai-sdk/commit/3ae5a527a425d114e9a38e26868c2189c667e974))

- **examples**: Fix typos and clarify reference types
  ([`833df4b`](https://github.com/caru-ini/novelai-sdk/commit/833df4b8ad997e94f622cbe390e4a8b84d1ee963))

- **examples**: Rename and update advanced reference example for precise references
  ([`8a6a973`](https://github.com/caru-ini/novelai-sdk/commit/8a6a973e7eab1cf000198d14a38942997086cb26))

- **examples**: Update character reference example with strength parameter
  ([`e9a0137`](https://github.com/caru-ini/novelai-sdk/commit/e9a01379b968dc138f67ef8af4529be0b322aa8d))

### Features

- **image**: Add strength parameter and style reference for precise reference
  ([`e04e17c`](https://github.com/caru-ini/novelai-sdk/commit/e04e17c6a1f175b49913564cbae9a58634b07893))

- **image**: Remove multiple character reference restriction
  ([`de7eea5`](https://github.com/caru-ini/novelai-sdk/commit/de7eea5103c8c44963bd533b2864d3fd0a7b7083))


## v0.4.3 (2026-01-18)

### Bug Fixes

- **position**: Correct character position calculation and update docs
  ([`1df170c`](https://github.com/caru-ini/novelai-sdk/commit/1df170c14566cd1cae219269536806e902064191))

### Documentation

- Add contributing guidelines in English and Japanese
  ([`e3d34bd`](https://github.com/caru-ini/novelai-sdk/commit/e3d34bd2d5dca79e55c04d2612ee96e1e263d60e))

- Explain two-layered data model architecture in README, website
  ([`d812200`](https://github.com/caru-ini/novelai-sdk/commit/d812200fa90274c4192a3cd8052a7cc8289ab03c))

- Fix i18n folder structure
  ([`8e1d4ab`](https://github.com/caru-ini/novelai-sdk/commit/8e1d4ab8b11fe1a9408594bf5662a40d209c6484))

- Update required python version
  ([`1058531`](https://github.com/caru-ini/novelai-sdk/commit/1058531afc7476906c6ef41c0432b6950323f8b6))

- **i18n**: Add simplified chinese(zh-hans) translation
  ([`69426ef`](https://github.com/caru-ini/novelai-sdk/commit/69426ef1ba701b57c62fbea3d20b79ed08b88f7c))

### Refactoring

- **constants**: Remove barrel file and use direct submodule imports
  ([`eb93069`](https://github.com/caru-ini/novelai-sdk/commit/eb9306918deb197cb6c0ce0dec1d925e0ba9bae2))

- **constants**: Standardize filenames to plural
  ([`9603ff6`](https://github.com/caru-ini/novelai-sdk/commit/9603ff6ba869e19196873e4fb7d7779913179ae3))


## v0.4.2 (2025-12-26)

### Bug Fixes

- Use object format for center coordinates in Multi-Character generation
  ([`d1d5a88`](https://github.com/caru-ini/novelai-sdk/commit/d1d5a88a0ca09c43320231193f9670363675969d))

### Chores

- Add issue and pull request templates
  ([`bcccf51`](https://github.com/caru-ini/novelai-sdk/commit/bcccf51b7906e3dbc93fdacf73d0215092943457))


## v0.4.1 (2025-12-25)

### Bug Fixes

- Use model_validator to validate character field
  ([`27ab2e1`](https://github.com/caru-ini/novelai-sdk/commit/27ab2e1ac82dfdc33aa9d65b06bdf950cfcd1ee0))


## v0.4.0 (2025-12-22)

### Bug Fixes

- Remove debug code
  ([`d8e4faf`](https://github.com/caru-ini/novelai-sdk/commit/d8e4faf4f2dee89b78874e302febd6481b46a820))

### Documentation

- Add competitor comparison table and update roadmap
  ([`d587053`](https://github.com/caru-ini/novelai-sdk/commit/d587053a5b86d8995e3f6551cd9a2b5cc28d17c5))

- Add wiki
  ([`4d05bd7`](https://github.com/caru-ini/novelai-sdk/commit/4d05bd76d07010782a255472b283d8d58a6cd73a))

- Fix incorrect ControlNet and i2i examples in documentation
  ([`663c4f4`](https://github.com/caru-ini/novelai-sdk/commit/663c4f4b3c56d35cf5e32555af9b99180f73ed57))

- Update japanese README
  ([`5984318`](https://github.com/caru-ini/novelai-sdk/commit/59843186bdfe37ff108ce01ac3731b68848ec7ea))

- **example**: Add FastAPI integration example and documentation
  ([`cad7175`](https://github.com/caru-ini/novelai-sdk/commit/cad7175f5d96e32599aea5f773a1b1592f77e7ec))

### Features

- Add image_format param
  ([`b88c4de`](https://github.com/caru-ini/novelai-sdk/commit/b88c4de93e8ced0ca6dc0083c07f86dbb70cf5bc))


## v0.3.0 (2025-12-16)

### Documentation

- Add AsyncNovelAI example
  ([`db42582`](https://github.com/caru-ini/novelai-sdk/commit/db42582220b76f609ee1c61e52f489936d4b5bc7))

- Update Controlnet subtitle for japanese
  ([`789c159`](https://github.com/caru-ini/novelai-sdk/commit/789c15977e00449db5f656c3771800e7fcc75190))

### Features

- **client**: Add AsyncNovelAI implementation
  ([`7702adb`](https://github.com/caru-ini/novelai-sdk/commit/7702adb5b939872c5074f47059c65cd0b72981a5))


## v0.2.3 (2025-11-09)

### Bug Fixes

- **image**: Use empty list when character_references is None
  ([`34a965f`](https://github.com/caru-ini/novelai-sdk/commit/34a965f916a9862c58e414e807ae183e78dee8c5))

### Chores

- **ci**: Prevent running release and deploy when pr open
  ([`d192a88`](https://github.com/caru-ini/novelai-sdk/commit/d192a8822bf70e29fc3a153aa40eeba776fce8fb))


## v0.2.2 (2025-11-07)

### Bug Fixes

- **ci**: Conditionally upload build artifacts based on release status
  ([`c8d39e4`](https://github.com/caru-ini/novelai-sdk/commit/c8d39e40a95f484e15aea6ee032c021990a8dbfe))

### Documentation

- **client**: Add comprehensive docstrings to NovelAI and ImageGeneration classes
  ([`0608a8d`](https://github.com/caru-ini/novelai-sdk/commit/0608a8d804fc7cce22f1c875c18d36f6380a3ba8))

### Refactoring

- **client**: Update API client initialization to include image, text, and main API base URLs
  ([`906395f`](https://github.com/caru-ini/novelai-sdk/commit/906395ff3c2789d0b0b2238a66b249652418536f))


## v0.2.1 (2025-11-07)

### Bug Fixes

- **ci**: Add output for release status in CI workflow
  ([`6d8e40c`](https://github.com/caru-ini/novelai-sdk/commit/6d8e40cb89f79ab0c3b438fb086152b2aacbb72e))


## v0.2.0 (2025-11-07)

### Chores

- Update CI workflow to exclude caru-bot from triggering jobs
  ([`e40caff`](https://github.com/caru-ini/novelai-sdk/commit/e40caff5b364b1231318d73ce8a906fd1d6aa900))

- Update version in uv.lock
  ([`927c789`](https://github.com/caru-ini/novelai-sdk/commit/927c789fe3864fa5924ecd18f2711ef381435a71))

- **ci**: Upgrade semantic-release actions to v10.4.1
  ([`6a7fa43`](https://github.com/caru-ini/novelai-sdk/commit/6a7fa43f9861269e70ee16446ae79e72825dc734))

- **deps**: Upgrade python-semantic-release to v10.2.0+
  ([`5d439a4`](https://github.com/caru-ini/novelai-sdk/commit/5d439a4e39cae4b25c8bbac9eb7268d21de297f1))

### Features

- Implement metadata eraser utility
  ([`2f4659c`](https://github.com/caru-ini/novelai-sdk/commit/2f4659c32c0e6c1e1ee749505b39c81e39daf05e))


## v0.1.0 (2025-11-07)

### Chores

- Lower Python version requirement to 3.10+
  ([`35800df`](https://github.com/caru-ini/novelai-sdk/commit/35800dfd62e0d1e9e80b611220365fd0ae7b22ac))

- Update CI workflow to use GitHub App instead
  ([`43fc179`](https://github.com/caru-ini/novelai-sdk/commit/43fc179d12bcc19264bc871539322441fba30387))

### Documentation

- Add README in Japanese
  ([`287cf6e`](https://github.com/caru-ini/novelai-sdk/commit/287cf6e042919abb7081cb51c1852c49938fd120))

- Fix typo
  ([`ec7dbd2`](https://github.com/caru-ini/novelai-sdk/commit/ec7dbd2731b7394021b1d45a2754d70b2c7c0bf4))

- Replace intro.png to new one
  ([`9d5ae16`](https://github.com/caru-ini/novelai-sdk/commit/9d5ae16613c8f973ceb9f4d9dfff69cc761cfe9a))

- Update terminology from "client" to "SDK" across documentation
  ([`923ec34`](https://github.com/caru-ini/novelai-sdk/commit/923ec34e8ff663980f154ad098a7413583c8b22a))

### Features

- Implement metadata extractor utility
  ([`29dad1a`](https://github.com/caru-ini/novelai-sdk/commit/29dad1a072559d8ae7e6bfd1a295511bb30b5495))

- **deps**: Add numpy to dependencies
  ([`f65ce14`](https://github.com/caru-ini/novelai-sdk/commit/f65ce14531d8df64c0e31514f5f81602221d0ff0))


## v0.0.2 (2025-11-02)

### Bug Fixes

- Include pyproject.toml version in version_variables
  ([`6e711f8`](https://github.com/caru-ini/novelai-sdk/commit/6e711f8f92d16eabd313c8d65ebc6792292d93b3))


## v0.0.1 (2025-11-02)

### Bug Fixes

- Update project urls
  ([`0b489fd`](https://github.com/caru-ini/novelai-sdk/commit/0b489fdb945692fbadba9dccdc48167443e5ed71))


## v0.0.0 (2025-11-02)

- Initial Release
