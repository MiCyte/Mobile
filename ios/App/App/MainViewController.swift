import UIKit
import Capacitor

/// The app's one screen: Capacitor's web view on https://micyte.com/dashboard/, plus the two
/// things a phone expects of it that a browser tab does not do by itself: pull down to
/// reload, and swipe from the edge to go back.
class MainViewController: CAPBridgeViewController {
    private let refresh = UIRefreshControl()

    override func capacitorDidLoad() {
        super.capacitorDidLoad()
        guard let webView = webView else { return }
        webView.allowsBackForwardNavigationGestures = true
        refresh.addTarget(self, action: #selector(reload), for: .valueChanged)
        webView.scrollView.refreshControl = refresh
    }

    @objc private func reload() {
        webView?.reload()
        refresh.endRefreshing()
    }
}
