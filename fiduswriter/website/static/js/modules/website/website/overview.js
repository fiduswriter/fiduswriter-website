import {whenReady, setDocTitle, getJson} from "../../common"
import {overviewBodyTemplate, overviewContentTemplate, websiteOverviewTitle} from "./templates"


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
        this.postsPerPage = false
        this.numPages = false
        this.downloadedPage = 0
    }

    init() {
        return this.getCSS().then(
            () => whenReady()
        ).then(
            () => this.readSettingsFromCSS()
        ).then(
            () => this.getPublications()
        ).then(
            () => this.render()
        ).then(
            () => this.bind()
        ).then(
            () => this.loadMore()
        )
    }

    getCSS() {
        return getJson("/api/website/get_style/").then(
            json => {
                if (json.style) {
                    const style = document.createElement("style")
                    style.innerHTML = json.style
                    document.head.appendChild(style)
                }
            }
        )
    }

    readSettingsFromCSS() {
        const postsPerPage = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--posts_per_page"))
        if (!isNaN(postsPerPage)) {
            this.postsPerPage = postsPerPage
        }
    }

    getPublications() {
        if (this.currentlyDownloadingPublications) {
            return false
        }
        this.currentlyDownloadingPublications = true
        const url = this.postsPerPage ? `/api/website/list_publications/${this.postsPerPage}/${this.downloadedPage + 1}/` : "/api/website/list_publications/"
        return getJson(url).then(
            json => {
                if (!this.downloadedPage) {
                    this.siteName = json.site_name
                    if (json.num_pages) {
                        this.numPages = json.num_pages
                    }
                }
                let keywords = [...this.keywords]
                let authors = [...this.authors]
                json.publications.forEach(publication => {
                    keywords = keywords.concat(publication.keywords)
                    authors = authors.concat(publication.authors)
                })
                this.publications = this.filteredPublications = this.publications.concat(json.publications)
                this.keywords = [...new Set(keywords)]
                this.authors = [...new Set(authors)]
                this.downloadedPage += 1
                this.currentlyDownloadingPublications = false
            }
        )
    }

    render() {
        this.dom = document.createElement("body")
        this.dom.classList.add("cms")
        this.renderBody()
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

    rerenderContent() {
        const contentDOM = this.dom.querySelector("div.content")
        contentDOM.innerHTML = overviewContentTemplate({
            keywords: this.keywords,
            authors: this.authors,
            publications: this.filteredPublications,
            filters: this.filters
        })
    }

    bind() {
        this.dom.addEventListener("click", event => {
            const authorEl = event.target.closest("span.author")
            const keywordEl = event.target.closest("span.keyword")
            if (!authorEl && !keywordEl) {
                return
            }
            event.preventDefault()
            if (authorEl) {
                if (authorEl.classList.contains("selected")) {
                    delete this.filters.author
                } else {
                    const index = parseInt(authorEl.dataset.index)
                    this.filters.author = this.authors[index]
                }
            } else {
                if (keywordEl.classList.contains("selected")) {
                    delete this.filters.keyword
                } else {
                    const index = parseInt(keywordEl.dataset.index)
                    this.filters.keyword = this.keywords[index]
                }
            }
            this.applyFilters()
            this.renderBody()

        })
        this.dom.addEventListener("scroll", () => {
            this.loadMore()
        })
    }

    loadMore() {
        if (this.dom.scrollTop + this.dom.clientHeight >= this.dom.scrollHeight) {
            if (this.numPages && this.numPages > this.downloadedPage) {
                this.getPublications().then(
                    () => this.rerenderContent()
                ).then(
                    () => this.loadMore()
                )
            }
        }
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
