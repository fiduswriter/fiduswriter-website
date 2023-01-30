import {whenReady, ensureCSS, setDocTitle, getJson} from "../../common"
import {articleBodyTemplate} from "./templates"


export class WebsiteArticle {

    constructor({app, user}, id) {
        this.app = app
        this.user = user
        this.id = id

        this.publication = {}
    }

    init() {
        return this.getPublication().then(
            () => whenReady()
        ).then(
            () => this.render()
        )
    }

    getPublication() {
        return getJson(`/api/website/get_publication/${this.id}/`).then(
            publication => this.publication = publication
        )
    }

    render() {
        this.dom = document.createElement("body")
        this.dom.classList.add("cms")
        this.dom.innerHTML = articleBodyTemplate({
            user: this.user,
            publication: this.publication
        })
        ensureCSS([
            staticUrl("css/document.css")
        ])
        document.body = this.dom
        setDocTitle(this.publication.title, this.app)
    }
}
