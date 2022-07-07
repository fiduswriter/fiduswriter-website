import {whenReady, ensureCSS, setDocTitle} from "../common"
import {baseBodyTemplate} from "./templates"


export class WebsiteOverview {

    constructor({app, user}) {
        this.app = app
        this.user = user

        this.publicationList = []
    }

    init() {
        return whenReady().then(() => {
            this.render()
        })
    }

    render() {
        this.dom = document.createElement('body')
        this.dom.classList.add('cms')
        this.dom.innerHTML = baseBodyTemplate({
            user: this.user
        })
        ensureCSS([
            'content_overview.css'
        ])
        document.body = this.dom
        setDocTitle(gettext('Documents'), this.app)
    }
}
