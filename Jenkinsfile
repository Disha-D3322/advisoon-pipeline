pipeline {
  agent any

  environment {
    LOG_DIR = "/tmp/advisoon-logs"
  }

  stages {
    stage('init') {
      steps {
        script {
          echo "==== INIT ===="
        }
        // ensure logs dir exists
        sh '''
          mkdir -p ${LOG_DIR}
          echo "Init at $(date)" > ${LOG_DIR}/init-$(date +%Y%m%d%H%M%S).log
        '''.replace('${LOG_DIR}','\\${LOG_DIR}')
      }
    }

    stage('pre-check') {
      steps {
        script {
          echo "Checking Python3 availability..."
          env.PY_CMD = sh(script: 'if command -v python3 >/dev/null 2>&1; then echo python3; elif command -v python >/dev/null 2>&1; then echo python; else echo ""; fi', returnStdout: true).trim()
          if (!env.PY_CMD) {
            error("Python not found on agent. Please install python3.")
          } else {
            echo "Using ${env.PY_CMD}"
            // write python version to log file; escape ${LOG_DIR} so Groovy doesn't interpolate it
            sh "${env.PY_CMD} --version | tee \\${LOG_DIR}/python-version-$(date +%Y%m%d%H%M%S).log"
          }
        }
      }
    }

    stage('test') {
      steps {
        script {
          echo "Running unit tests with pytest..."
          def TS = sh(script: "date +%Y%m%d%H%M%S", returnStdout: true).trim()
          env.RUN_TS = TS
          // Use escaped ${LOG_DIR} and ${RUN_TS} inside the here-doc so Groovy doesn't interpret them
          sh '''
            set -e
            mkdir -p reports logs
            ${PY_CMD} -m pytest -q --junitxml=reports/junit-${RUN_TS}.xml || true
            ${PY_CMD} -m pytest -q > logs/pytest-${RUN_TS}.log 2>&1 || true
            echo "Test run saved to logs/pytest-${RUN_TS}.log"
          '''.replace('${PY_CMD}','${env.PY_CMD}').replace('${RUN_TS}','${TS}').replace('${LOG_DIR}','\\${LOG_DIR}')
        }
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: "reports/junit-*.xml"
        }
      }
    }

    stage('verify') {
      steps {
        script {
          echo "Verify: run lint / quick static checks (optional)"
          sh '''
            TS=${RUN_TS:-$(date +%Y%m%d%H%M%S)}
            ${PY_CMD} -c "from ad_scoring import score_ad; print(score_ad({'ctr':0.03,'relevance':0.9,'budget_ratio':0.7}))" > logs/verify-${TS}.txt
            echo "verify completed"
          '''.replace('${PY_CMD}','${env.PY_CMD}').replace('${RUN_TS}','${env.RUN_TS}')
        }
      }
    }

    stage('publish') {
      steps {
        script {
          echo "Publish: archive artifacts into ${LOG_DIR} with timestamped names"
          sh '''
            TS=${RUN_TS:-$(date +%Y%m%d%H%M%S)}
            mkdir -p ${LOG_DIR}
            cp -v logs/* ${LOG_DIR}/ || true
            cp -v reports/* ${LOG_DIR}/ || true
            for f in ${LOG_DIR}/*; do
              if [[ "$f" != *${TS}* ]]; then
                mv "$f" "${f%.*}-${TS}.${f##*.}" || true
              fi
            done
            echo "Published artifacts to ${LOG_DIR}"
          '''.replace('${RUN_TS}','${env.RUN_TS}').replace('${LOG_DIR}','\\${LOG_DIR}')
        }
      }

      post {
        success {
          archiveArtifacts artifacts: '/tmp/advisoon-logs/**', fingerprint: true
        }
        always {
          sh 'ls -lah /tmp/advisoon-logs || true'
        }
      }
    }
  } // stages

  post {
    always {
      echo "Pipeline finished at $(date)"
    }
  }
}
