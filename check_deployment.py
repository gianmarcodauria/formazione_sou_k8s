import yaml
from kubernetes import client, config

# Carica kubeconfig corretto
config.load_kube_config(config_file="kubeconfig_test_copia")

v1 = client.AppsV1Api()

DEPLOYMENT_NAME = "flask-app"
NAMESPACE = "formazione-sou"

try:
    deployment = v1.read_namespaced_deployment(name=DEPLOYMENT_NAME, namespace=NAMESPACE)
except client.exceptions.ApiException as e:
    print(f"Errore: {e}")
    exit(1)

containers = deployment.spec.template.spec.containers
errors = []

for c in containers:
    if not c.liveness_probe:
        errors.append(f"{c.name}: livenessProbe mancante")
    if not c.readiness_probe:
        errors.append(f"{c.name}: readinessProbe mancante")
    if not c.resources or not c.resources.limits or not c.resources.requests:
        errors.append(f"{c.name}: resources limits/requests mancanti")

if errors:
    print("Errore: il Deployment non rispetta le best practice:")
    for e in errors:
        print("-", e)
    exit(1)

print(f"Deployment {DEPLOYMENT_NAME} conforme alle best practice")
