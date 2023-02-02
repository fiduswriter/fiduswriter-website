import {whenReady, ensureCSS, setDocTitle, getJson} from "../../common"
import {articleBodyTemplate} from "./templates"


export class WebsiteArticle {

    constructor({app, user}, id) {
        this.app = app
        this.user = user
        this.id = id

        this.siteName = "" // Name of site as stored in database.

        this.publication = {}
        this.popUp = false
    }

    init() {
        return this.getPublication().then(
            () => whenReady()
        ).then(
            () => this.render()
        ).then(
            () => this.bind()
        )
    }

    getPublication() {
        return getJson(`/api/website/get_publication/${this.id}/`).then(
            json => {
                this.publication = json.publication
                this.siteName = json.site_name
            }
        )
    }

    render() {
        this.dom = document.createElement("body")
        this.dom.classList.add("article")
        this.dom.innerHTML = articleBodyTemplate({
            user: this.user,
            siteName: this.siteName,
            publication: this.publication
        })
        ensureCSS([
            staticUrl("css/document.css")
        ])
        document.body = this.dom
        setDocTitle(this.publication.title, this.app)
    }

    bind() {
        this.dom.addEventListener("click", event => {
            const target = event.target
            if (this.popUp && !this.popUp.contains(target)) {
                this.dom.removeChild(this.popUp)
                this.popUp = false
            }
            const link = target.closest("a")
            if (!link) {
                return
            }
            const href = link.getAttribute("href")
            if (!href || href[0] !== "#") {
                return
            }
            event.preventDefault()
            event.stopPropagation()
            const linkRef = this.dom.querySelector(href)
            if (linkRef) {
                if (this.popUp) {
                    if (this.popUp.firstElementChild !== this.popUp.lastElementChild) {
                        this.popUp.removeChild(this.popUp.lastElementChild)
                    }
                } else {
                    this.popUp = document.createElement("div")
                    this.popUp.classList.add("popup")
                    this.popUp.style.position = "absolute"
                    this.popUp.style.top = `${event.clientY + this.dom.scrollTop + 10}px`
                    this.popUp.style.left = `${event.clientX + 10}px`
                }
                this.popUp.innerHTML += linkRef.outerHTML
                this.dom.appendChild(this.popUp)
            }
        })
    }
}
