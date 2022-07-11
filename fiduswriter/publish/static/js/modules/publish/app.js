export class AppPublish {
    constructor(app) {
        this.app = app
    }

    init() {
        this.app.routes[""] = {
            app: "publish",
            requireLogin: false,
            open: () => import(/* webpackPrefetch: true */"./website/overview").then(({WebsiteOverview}) => new WebsiteOverview(this.app.config))
        }
        this.app.routes["article"] = {
            app: "publish",
            requireLogin: false,
            open: pathnameParts => {
                let id = pathnameParts.pop()
                if (!id.length) {
                    id = pathnameParts.pop()
                }
                return import(/* webpackPrefetch: true */"./website/article").then(({WebsiteArticle}) => new WebsiteArticle(this.app.config, id))
            }
        }
    }
}
