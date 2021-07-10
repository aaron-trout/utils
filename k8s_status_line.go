package main

import (
	"fmt"
	"io/ioutil"
	"os/user"

	"gopkg.in/yaml.v3"
)

// KubeConfig represents the kubectl config file at ~/.kube/config
type KubeConfig struct {
	CurrentContext string `yaml:"current-context"`
	Contexts []KubeContext `yaml:"contexts"`
}

// KubeContext is a context definition from kubeconfig
type KubeContext struct {
	Name string `yaml:"name"`
	Config map[string]string `yaml:"context"`
}

func findNamespace(contextName string, kubeconfig KubeConfig) (namespaceName string) {
	for _, context := range kubeconfig.Contexts {
		if context.Name == contextName {
			namespace, exists := context.Config["namespace"]
			if exists {
				return namespace
			}
		}
	}
	return "default"
}

func kubeConfigPath() (string) {
	// TODO: Support KUBECONFIG env var
	user, _ := user.Current()
	return user.HomeDir + "/.kube/config"
}

func main() {
	kubeconfig := KubeConfig{}

	// Load file contents
	data, err := ioutil.ReadFile(kubeConfigPath())
	if err != nil {
		panic("Error reading kubeconfig")
	}

	// Decode YAML
	err = yaml.Unmarshal([]byte(data), &kubeconfig)
	if err != nil {
		panic("Error decoding YAML of kubeconfig")
	}

	// Output context name and namespace
	namespace := findNamespace(kubeconfig.CurrentContext, kubeconfig)
	fmt.Println(kubeconfig.CurrentContext + "/" + namespace)
}
