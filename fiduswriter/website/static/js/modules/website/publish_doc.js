import {postJson} from "../common"
import {HTMLExporter} from "../exporter/html2"

import {htmlExportTemplate} from "./templates"

// Send the HTML version of a document to the server for publication as a webpage.
export class PublishDoc extends HTMLExporter {
    constructor(url, user, message, authors, keywords, abstract, ...exporterArgs) {
        const returnValue = super(...exporterArgs)
        this.url = url
        this.user = user
        this.message = message
        this.authors = authors
        this.keywords = keywords
        this.abstract = abstract
        this.htmlExportTemplate = htmlExportTemplate
        return returnValue
    }
    download(blob) {
        return postJson(
            this.url,
            {
                doc_id: this.doc.id,
                title: this.docTitle,
                authors: this.authors,
                keywords: this.keywords,
                abstract: this.abstract,
                "html.zip": {file: blob, filename: "html.zip"},
                message: this.message
            }
        )
    }
}
