import {whenReady, ensureCSS, setDocTitle, getJson} from "../../common"
import {overviewBodyTemplate, websiteOverviewTitle} from "./templates"


export class WebsiteOverview {

    constructor({app, user}) {
        this.app = app
        this.user = user

        this.publications = []
    }

    init() {
        return this.getPublications().then(
            () => whenReady()
        ).then(
            () => this.render()
        )
    }

    getPublications() {
        return getJson('/api/publish/list_publications').then(
            json => this.publications = json.publications
        )
    }

    render() {
        this.dom = document.createElement('body')
        this.dom.classList.add('cms')
        this.dom.innerHTML = overviewBodyTemplate({
            user: this.user,
            publications: this.publications
        })
        ensureCSS([
            'website_overview.css'
        ])
        document.body = this.dom
        setDocTitle(websiteOverviewTitle, this.app)
    }
}
