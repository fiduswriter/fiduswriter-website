export class AppWebsite {
    constructor(app) {
        this.app = app
    }

    init() {
        this.app.routes[""] = {
            app: "website",
            requireLogin: false,
            open: () => import(/* webpackPrefetch: true */"./website/overview").then(({WebsiteOverview}) => new WebsiteOverview(this.app.config))
        }
        this.app.routes["article"] = {
            app: "website",
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
