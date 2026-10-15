# SFL with the reF1nd core

The `SFL reF1nd Linux amd64 deb` Actions workflow builds only the Linux
amd64 Debian package. It uses the existing desktop packaging command:

```sh
pnpm package:linux:deb x64
```

The desktop source is checked out beside `reF1nd/sing-box`, pinned to
`78ea0ce9257bd3bedd4d1185d6cc4723f04096b4` from `reF1nd-testing`.
The existing scripts generate the desktop and dashboard RPC bindings from
that core and compile `experimental/boxdd` into `sing-box-daemon`.
The ordinary sing-box CLI is not substituted for the desktop daemon.

Run the workflow from the Actions tab on branch `ref1nd-linux-amd64`.
It also runs when that branch receives a push. Download the
`SFL-ref1nd-linux-amd64` artifact after the workflow succeeds. It contains:

- `SFL-1.14.3-ref1nd.1-amd64.deb`
- SHA256 checksums, source revisions and core module build information
- A matching command line binary for checking configurations

The workflow verifies the Debian architecture, compares the packaged daemon
against the compiled daemon, checks for reF1nd dependencies in its Go build
information, and provides a matching CLI for local configuration validation.
It does not publish a release or install anything on the local computer.

This package keeps upstream's application identity and service paths, so it
replaces the installed original SFL. Back up existing profiles before installing.

