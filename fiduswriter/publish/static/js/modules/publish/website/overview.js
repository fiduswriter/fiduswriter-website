import {whenReady, ensureCSS, setDocTitle, getJson} from "../../common"
import {overviewBodyTemplate, websiteOverviewTitle} from "./templates"


export class WebsiteOverview {

    constructor({app, user}) {
        this.app = app
        this.user = user

        this.siteName = "" // Name of site as stored in database.
        this.publications = [] // Publications as they come from the server

        this.authors = [] // Every author used in at least one publication
        this.keywords = [] // Every keyword used in at least one publication

        this.filters = {} // current applied filters
        this.filteredPublications = [] // Shortened publication list after applying filters.
    }

    init() {
        return this.getPublications().then(
            () => whenReady()
        ).then(
            () => this.render()
        ).then(
            () => this.bind()
        )
    }

    getPublications() {
        return getJson('/api/publish/list_publications/').then(
            json => {
                this.siteName = json.site_name
                let keywords = []
                let authors = []
                json.publications.forEach(publication => {
                    keywords = keywords.concat(publication.keywords)
                    authors = authors.concat(publication.authors)
                })
                this.publications = json.publications
                this.filteredPublications = json.publications
                this.keywords = [...new Set(keywords)]
                this.authors = [...new Set(authors)]
            }
        )
    }

    render() {
        this.dom = document.createElement('body')
        this.dom.classList.add('cms')
        this.renderBody()
        ensureCSS([
            'website_overview.css'
        ])
        document.body = this.dom
        setDocTitle(websiteOverviewTitle, this.app)
    }

    renderBody() {
        this.dom.innerHTML = overviewBodyTemplate({
            user: this.user,
            siteName: this.siteName,
            authors: this.authors,
            keywords: this.keywords,
            publications: this.filteredPublications,
            filters: this.filters
        })
    }

    bind() {
        this.dom.addEventListener('click', event => {
            const authorEl = event.target.closest('span.author')
            const keywordEl = event.target.closest('span.keyword')
            if (!authorEl && !keywordEl) {
                return
            }
            event.preventDefault()
            if (authorEl) {
                if (authorEl.classList.contains('selected')) {
                    delete this.filters.author
                } else {
                    const index = parseInt(authorEl.dataset.index)
                    this.filters.author = this.authors[index]
                }
            } else {
                if (keywordEl.classList.contains('selected')) {
                    delete this.filters.keyword
                } else {
                    const index = parseInt(keywordEl.dataset.index)
                    this.filters.keyword = this.keywords[index]
                }
            }
            this.applyFilters()
            this.renderBody()

        })
    }

    applyFilters() {
        this.filteredPublications = this.publications.filter(publication => {
            if (this.filters.author && !publication.authors.includes(this.filters.author)) {
                return false
            }
            if (this.filters.keyword && !publication.keywords.includes(this.filters.keyword)) {
                return false
            }
            return true
        })
    }
}
