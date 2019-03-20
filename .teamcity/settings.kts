import jetbrains.buildServer.configs.kotlin.v2018_2.*
import jetbrains.buildServer.configs.kotlin.v2018_2.triggers.vcs
import jetbrains.buildServer.configs.kotlin.v2018_2.buildSteps.script

version = "2018.2"

project {

    buildType(Build)
}

object Build : BuildType({
    name = "Build"

    vcs {
        root(DslContext.settingsRoot)
    }

    triggers {
        vcs {
        }
    }
    steps {
        script {
            name = "pip install"
            dockerImage = "python:3.6"
            scriptContent = "pip install -r requirements.txt"
        }
        script {
            name = "py tests"
            dockerImage = "python:3.6"
            scriptContent = "python -m unittest discover -s ./ -p 'test_*.py'"
        }
    }
})
