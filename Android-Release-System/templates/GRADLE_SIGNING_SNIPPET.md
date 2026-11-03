# Groovy `build.gradle` release-signing pattern

Use the equivalent of this in a Groovy Android app build script. Adapt only syntax that genuinely differs for the project's Gradle/AGP setup.

```groovy
def releaseStore = System.getenv('ANDROID_RELEASE_KEYSTORE')
def releaseStorePassword = System.getenv('ANDROID_RELEASE_STORE_PASSWORD')
def releaseKeyAlias = System.getenv('ANDROID_RELEASE_KEY_ALIAS')
def releaseKeyPassword = System.getenv('ANDROID_RELEASE_KEY_PASSWORD')
def releaseSigningReady = [releaseStore, releaseStorePassword, releaseKeyAlias, releaseKeyPassword].every {
    it != null && !it.trim().isEmpty()
}

android {
    if (releaseSigningReady) {
        signingConfigs {
            release {
                storeFile file(releaseStore)
                storePassword releaseStorePassword
                keyAlias releaseKeyAlias
                keyPassword releaseKeyPassword
                enableV1Signing true
                enableV2Signing true
                enableV3Signing true
                enableV4Signing true
            }
        }
    }

    buildTypes {
        debug {
            applicationIdSuffix '.dev'
            versionNameSuffix '-dev'
        }
        release {
            if (!releaseSigningReady) {
                // Do not attach a debug/fallback signer here.
            } else {
                signingConfig signingConfigs.release
            }
        }
    }
}

tasks.register('verifyPermanentReleaseSigningReady') {
    doLast {
        if (!releaseSigningReady) {
            throw new GradleException('Permanent Android signing identity is unavailable. Release blocked.')
        }
    }
}

afterEvaluate {
    tasks.matching { it.name == 'preReleaseBuild' }.configureEach {
        dependsOn tasks.named('verifyPermanentReleaseSigningReady')
    }
}
```

The reusable GitHub workflow independently verifies the final APK signer/package/version after build. Both layers are intentional: the project must fail closed before/during release, and the finished APK identity must also be verified before publication.
