pipeline {
    agent any
    stages {
        stage("clean") {
            steps {
                sh 'rm -rf ./dist/*'
            }
        }
        stage("install") {
            steps {
                sh 'mamba env update --file environment.yml || mamba env create --force --file environment.yml'
                sh 'echo "mamba activate bmlsa" >> ~/.bashrc'
            }
        }
        stage("unit tests") {
            steps {
                sh "python -m pytest --junitxml=test_results.xml"
                xunit checksName: '', tools: [JUnit(excludesPattern: '', pattern: 'test_results.xml', stopProcessingIfError: true)]
            }
        }
        stage("build") {
            steps {
                sh "python -m build"
            }
        }
        stage("test installation") {
            steps {
                sh "pip install dist/*.whl --force-reinstall"
                sh "bmlsa -h"
                sh "bmlsa -I id -S sequence -B BLASTp tests/resources/SARS_CoV-2_genes.csv tests/resources/NC_045512_coding.fasta /output/"
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
                withCredentials([usernamePassword(credentialsId: 'rs-git-package-registry-ydeng', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh returnStatus: true, script: 'python -m twine upload --repository-url https://git.reslate.systems/api/packages/${USER}/pypi -u ${USER} -p ${PASS} --non-interactive --disable-progress-bar --verbose dist/*'
                }
            }
        }
    }
}