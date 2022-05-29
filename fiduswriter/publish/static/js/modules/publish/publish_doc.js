import {post} from "../common"

import {HTMLExporter} from "../exporter/html"

// Send the HTML version of a document to the server for publication as a webpage.
export class PublishDoc extends HTMLExporter {
    download(blob) {
        return post(
            '/api/publish/publish_doc/',
            {id: this.doc.id,
                zip: blob
            }
        )
    }
}
