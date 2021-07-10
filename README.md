# Utils

A collection of random utility programs, written in Go.

## k8s_status_line

I have my current kubectl context and namespace displayed in my tmux status
line so that I know where my kubectl commands are going to be targeted by
default. Previously I was using `kubectl` and `jq` like so:

`set -g status-right "#(kubectl config current-context)/#(kubectl config view --minify -o=json | jq -r '.contexts[0].context.namespace')`

Combined, those commands take around 250ms on my machine:

```bash
$ time kubectl config current-context
microk8s
kubectl config current-context  0.03s user 0.04s system 47% cpu 0.148 total
$ time kubectl config view --minify -o=json | jq -r '.contexts[0].context.namespace'
default
kubectl config view --minify -o=json  0.05s user 0.01s system 113% cpu 0.049 total
jq -r '.contexts[0].context.namespace'  0.03s user 0.00s system 61% cpu 0.048 total
```

The `k8s_status_line` utility directly reads the `~/.kube/config` file and
produces output in the format: `<current_context>/<default_namespace>`. As
you can see it is much faster:

```bash
$ time ./k8s_status_line
microk8s/default
./k8s_status_line  0.00s user 0.00s system 71% cpu 0.009 total
```

Only 9ms! That's a 236ms saving compared with the `kubectl` + `jq` version!

### Limitations

- Currently it will only read `~/.kube/config` and does not support
    `$KUBECONFIG`

### Downloads

[![K8s Status Line](https://github.com/aaron-trout/utils/actions/workflows/k8s_status_line.yaml/badge.svg)](https://github.com/aaron-trout/utils/actions/workflows/k8s_status_line.yaml)

Find the latest GitHub actions build and download the binary for your platform:
https://github.com/aaron-trout/utils/actions/workflows/k8s_status_line.yaml?query=branch%3Amaster
