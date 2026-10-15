# SFL with the reF1nd core

This fork follows two upstreams:

- Desktop: the desktop commit pinned by the paired stable SagerNet release
- Core: `reF1nd/sing-box`, stable tags `vX.Y.Z-reF1nd`

The **Follow SFL and reF1nd upstreams** Actions workflow checks both daily
at 06:00 Singapore time. It resolves the newest stable reF1nd tag and its matching stable SagerNet release,
records both source commits in `ref1nd-core.json`, and builds a new Linux amd64 deb
when the paired stable release changes. Desktop `main` and core `testing` are not
used as build sources. It can also be run manually, including a forced
build when neither source changed. A missing or prerelease upstream pair stops the workflow; synchronization never force-pushes.

The reusable **SFL reF1nd Linux amd64 deb** workflow builds only:

```sh
pnpm package:linux:deb x64
```

The desktop source is checked out beside the pinned core. Existing scripts
generate desktop and dashboard RPC bindings from that core and compile
`experimental/boxdd` into `sing-box-daemon`. The ordinary sing-box CLI is
not substituted for the desktop daemon.

Download the `SFL-ref1nd-linux-amd64` artifact from a successful run. It contains:

- `SFL-<upstream-version>+ref1nd.<UTC-build-timestamp>-amd64.deb`
- SHA256 checksums, source revisions and core module build information
- A matching command line binary for local configuration validation

The build verifies the Debian architecture, compares the packaged daemon
against the compiled daemon, and checks for reF1nd dependencies in its Go
build information. Personal configurations and derived examples are not included
in the repository or the build inputs.

The package keeps upstream's application identity and service paths, replacing
the original SFL when installed. Building does not install it locally or publish
a GitHub release. Artifacts are retained for 30 days.

The build verifies the exact stable daemon version. Future upstream
API or toolchain changes may require a build fix; failures remain visible in
Actions instead of producing an unchecked package.
