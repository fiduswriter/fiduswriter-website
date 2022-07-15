import {postJson} from "../common"

import {HTMLExporter} from "../exporter/html"

// Send the HTML version of a document to the server for publication as a webpage.
export class PublishDoc extends HTMLExporter {
    constructor(user, message, ...exporterArgs) {
        const returnValue = super(...exporterArgs)
        this.user = user
        this.message = message
        return returnValue

    }
    download(blob) {
        const authors = this.doc.content.content.filter(
            part => part.attrs.metadata === 'authors'
        ).map(
            authorPart => authorPart.content ?
                authorPart.content.filter(
                    author => !author.marks || !author.marks.find(mark => mark.type === 'deletion')
                ).map(author => `${author.attrs.firstname} ${author.attrs.lastname}`) :
                []
        ).flat()
        if (!authors.length) {
            authors.push(this.user.name)
        }
        const keywords = this.doc.content.content.filter(
            part => part.attrs.metadata === 'keywords'
        ).map(
            keywordPart => keywordPart.content ?
                keywordPart.content.filter(
                    keyword => !keyword.marks || !keyword.marks.find(mark => mark.type === 'deletion')
                ).map(keyword => keyword.attrs.tag) :
                []
        ).flat()
        return postJson(
            '/api/publish/publish_doc/',
            {
                doc_id: this.doc.id,
                title: this.docTitle,
                authors,
                keywords,
                'html.zip': {file: blob, filename: 'html.zip'},
                message: this.message
            }
        )
    }
}
