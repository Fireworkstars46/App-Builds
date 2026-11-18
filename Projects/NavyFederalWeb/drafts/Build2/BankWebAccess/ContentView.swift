import SwiftUI
import SafariServices

// The banking website is always opened by Apple's browser UI.
// No account API, webview scripting, traffic interception or credential handling.
private enum OfficialWebsite {
    static let url = URL(string: "https://www.navyfederal.org/")!
}

struct ContentView: View {
    @State private var showWebsite = false
    @State private var launchedOnce = false

    var body: some View {
        VStack(spacing: 18) {
            Spacer(minLength: 20)

            Image(systemName: "lock.shield")
                .font(.system(size: 60))
                .foregroundStyle(.blue)
                .accessibilityHidden(true)

            Text("Navy Federal")
                .font(.largeTitle.bold())
                .multilineTextAlignment(.center)

            Text("Unofficial personal-use website launcher")
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)

            Text("Open Navy Federal Credit Union's official online banking website in Apple's Safari browser view.")
                .multilineTextAlignment(.center)
                .fixedSize(horizontal: false, vertical: true)
                .padding(.horizontal)

            Text("www.navyfederal.org")
                .font(.footnote.monospaced())
                .foregroundStyle(.secondary)
                .accessibilityLabel("Official website: www dot navyfederal dot org")

            Button {
                showWebsite = true
            } label: {
                Label("Open Online Banking", systemImage: "globe")
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 7)
            }
            .buttonStyle(.borderedProminent)
            .controlSize(.large)
            .padding(.horizontal, 28)

            Button {
                UIApplication.shared.open(OfficialWebsite.url)
            } label: {
                Label("Open in Safari Instead", systemImage: "safari")
            }
            .buttonStyle(.bordered)

            Spacer()

            Text("This is NOT Navy Federal's official app and is not affiliated with or endorsed by Navy Federal Credit Union. It never collects or stores passwords or account details. Verify the displayed website address before signing in.")
                .font(.caption)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
                .fixedSize(horizontal: false, vertical: true)
                .padding(.horizontal, 24)
                .padding(.bottom, 18)
        }
        .padding(.top, 12)
        .task {
            if !launchedOnce {
                launchedOnce = true
                showWebsite = true
            }
        }
        .fullScreenCover(isPresented: $showWebsite) {
            SecureSafariView(url: OfficialWebsite.url, isPresented: $showWebsite)
        }
    }
}

private struct SecureSafariView: UIViewControllerRepresentable {
    let url: URL
    @Binding var isPresented: Bool

    func makeUIViewController(context: Context) -> SFSafariViewController {
        let browser = SFSafariViewController(url: url)
        browser.dismissButtonStyle = .done
        browser.delegate = context.coordinator
        return browser
    }

    func updateUIViewController(_ browser: SFSafariViewController, context: Context) { }

    func makeCoordinator() -> Coordinator {
        Coordinator(isPresented: $isPresented)
    }

    final class Coordinator: NSObject, SFSafariViewControllerDelegate {
        @Binding var isPresented: Bool

        init(isPresented: Binding<Bool>) { _isPresented = isPresented }

        func safariViewControllerDidFinish(_ controller: SFSafariViewController) {
            isPresented = false
        }
    }
}
