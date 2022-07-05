export class AppPublish {
    constructor(app) {
        this.app = app
    }

    init() {
        this.app.routes[""] = {
            app: "publish",
            requireLogin: false,
            open: () => import(/* webpackPrefetch: true */"./overview").then(({WebsiteOverview}) => new WebsiteOverview(this.app.config))
        }
    }
}
