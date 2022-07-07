import {postJson} from "../common"

import {HTMLExporter} from "../exporter/html"

// Send the HTML version of a document to the server for publication as a webpage.
export class PublishDoc extends HTMLExporter {
    constructor(message, ...exporterArgs) {
        const returnValue = super(...exporterArgs)
        this.message = message
        return returnValue

    }
    download(blob) {
        return postJson(
            '/api/publish/publish_doc/',
            {
                doc_id: this.doc.id,
                'html.zip': {file: blob, filename: 'html.zip'},
                message: this.message
            }
        )
    }
}
