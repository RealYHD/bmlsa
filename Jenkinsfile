pipeline {
    agent {
        kubernetes {
            cloud 'rsys-devel'
            defaultContainer 'pip'
            inheritFrom 'pip'
        }
    }

    stages {
        stage("install") {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage("unit tests") {
            steps {
                sh returnStatus: true, script: "python -m pytest --junitxml=test_results.xml"
                xunit checksName: '', tools: [JUnit(excludesPattern: '', pattern: 'test_results.xml', stopProcessingIfError: true)]
            }
        }
        stage("build") {
            steps {
                sh 'rm -rf ./dist/*'
                sh 'rm -rf ./docs/build/*'
                sh "python -m build"
                container('sphinx') {
                    sh 'sphinx-apidoc -o docs/source/autodoc/bmlsa src/bmlsa --force'
                    sh 'sphinx-build -M html ./docs/source ./docs/build'
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'docs/build/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                }
            }
        }
        stage("test installation") {
            steps {
                sh "pip install dist/*.whl --force-reinstall"
                sh "bmlsa -h"
                sh "bmlsa -I id -S sequence -B BLASTp tests/resources/SARS_CoV-2_genes.csv tests/resources/NC_045512_coding.fasta ./output/"
            }
        }
        stage("archive") {
            steps {
                archiveArtifacts artifacts: 'dist/*.tar.gz, dist/*.whl', fingerprint: true, followSymlinks: false, onlyIfSuccessful: true
            }
        }
        stage("publish") {
            when {
                branch '**/master'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: '4d6f64be-d26d-4f95-8de3-b6a9b0beb311', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh returnStatus: true, script: 'python -m twine upload --repository-url https://git.reslate.systems/api/packages/${USER}/pypi -u ${USER} -p ${PASS} --non-interactive --disable-progress-bar --verbose dist/*'
                }
            }
        }
    }
}