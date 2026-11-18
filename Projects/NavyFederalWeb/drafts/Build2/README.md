# Navy Federal (Unofficial website launcher) - v1.0 Build 2

Personal-use, non-affiliated app. This is a correction of the **Bank Web Access v1.0 Build 1 source draft**. The unique project bundle identifier remains `com.fireworkstars46.bankwebaccess`. Version is 1.0; Build is incremented to 2 because the Home Screen name and AppIcon were requested changes.

- Home Screen label: **Navy Federal** (the official listing's full title is **Navy Federal Credit Union**).
- The icon is generated from the verified App Store listing id 370811491 by the build job; image provenance and SHA-256 recorded with generated icon files.
- Opens the official `https://www.navyfederal.org/` website in `SFSafariViewController`; Safari fallback button.
- No WKWebView, interception, login forms, password/secret storage, APIs, analytics or account data.
- iOS 16+ iPhone target, unsigned IPA intended for a user-managed Sideloadly signing workflow.
- Website compatibility, login/MFA and device behavior require personal iPhone testing; not yet verified.
- This code is not an official Navy Federal app. Brand icon is used for the owner's personal shortcut; do not publish or represent it as endorsed.

An unsigned IPA is **not signed or directly installable**. The owner's Sideloadly workflow performs Apple ID signing; update compatibility and signer verification, backup/recovery if applicable, testing and archival release gates still apply. Status remains **NOT DONE** until those gates pass.

Source is on the `wip/navy-federal-web-build2` working branch. The intended CI workflow generates icons via Apple's listing, builds with Xcode on macOS, packages Payload/BankWebAccess.app, checks info.plist + icons and reports hashes. If Apple listing/content retrieval or compilation fails, workflow must fail rather than supplying an invalid IPA.
