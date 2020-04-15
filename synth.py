import synthtool as s
import synthtool.gcp as gcp
import logging
import subprocess

logging.basicConfig(level=logging.DEBUG)

AUTOSYNTH_MULTIPLE_COMMITS = True


gapic = gcp.GAPICMicrogenerator()
version = 'v1'
library = gapic.typescript_library(
    'datastore', version,
    generator_args={
        "grpc-service-config": f"google/datastore/{version}/datastore_grpc_service_config.json",
        "package-name": "@google-cloud/datastore",
        "main-service": "datastore"
        },
        proto_path=f'/google/datastore/{version}',
        extra_proto_files=['google/cloud/common_resources.proto'],
    )

# Copy everything except for top level index, package.json, and README.md
s.copy(
    library,
    excludes=['package.json', 'README.md', 'src/index.ts'])

common_templates = gcp.CommonTemplates()
templates = common_templates.node_library(source_location="build/src")
s.copy(templates)

# Node.js specific cleanup
subprocess.run(['npm', 'install'])
subprocess.run(['npm', 'run', 'fix'])
subprocess.run(['npx', 'compileProtos', 'src'])
