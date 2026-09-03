// Declarative Jenkins pipeline mirroring .github/workflows/ci.yml stage-for-stage, so both
// CI systems exercise the same suite. See README "Jenkinsfile -- full walkthrough" for how
// to run this against a local Jenkins instance (no company Jenkins server needed).
pipeline {
    // Runs inside the official Playwright image so Chromium/Firefox/WebKit's OS-level
    // dependencies are already present -- nothing to install on the Jenkins host itself.
    // Keep this tag in sync with the playwright== version pinned in requirements.txt.
    agent {
        docker { image 'mcr.microsoft.com/playwright/python:v1.62.0-noble' }
    }

    // Runs nightly on a schedule; can also be triggered manually from Jenkins.
    triggers {
        cron('H 2 * * *')
    }

    environment {
        BASE_URL = 'https://automationexercise.com'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Install Playwright browsers') {
            steps {
                // Already present in the base image; kept explicit so the pipeline is
                // self-contained if the agent image is ever swapped for a plain Python one.
                sh '''
                    . venv/bin/activate
                    playwright install --with-deps
                '''
            }
        }

        stage('Run tests') {
            steps {
                // "|| true" keeps the pipeline going even if tests fail.
                // The real pass/fail result lives in the report and in
                // the post block below, not in this shell step's exit code.
                sh '''
                    . venv/bin/activate
                    pytest -m "smoke or regression or api" \
                        --alluredir=reports/allure-results \
                        --junitxml=reports/junit.xml || true
                '''
            }
        }

        stage('Generate report') {
            // Requires the Allure commandline tool on the agent (not bundled in the
            // Playwright image). Install it via the Jenkins "Allure Commandline" tool
            // plugin, or add an `npm install -g allure-commandline` step above, before
            // relying on this stage -- see README "Known limitations & next steps".
            steps {
                sh '''
                    . venv/bin/activate
                    allure generate reports/allure-results -o reports/allure-report --clean
                '''
            }
        }
    }

    post {
        always {
            // Attaches the HTML report and JUnit results to this build.
            archiveArtifacts(
                artifacts: 'reports/allure-report/**',
                allowEmptyArchive: true
            )
            junit testResults: 'reports/junit.xml', allowEmptyResults: true
        }
        failure {
            echo 'Build failed -- check the archived Allure report for details.'
        }
    }
}
