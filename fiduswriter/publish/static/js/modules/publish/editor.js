import {addAlert, postJson, Dialog} from "../common"
import {submitDialogTemplate} from "./templates"
import {PublishDoc} from "./publish_doc"
import {READ_ONLY_ROLES, COMMENT_ONLY_ROLES} from "../editor"

// Adds functions for Publishing to the editor
export class EditorPublish {
    constructor(editor) {
        this.editor = editor
        this.submission = {
            status: 'unknown'
        }
    }

    init() {
        const docData = {
            doc_id: this.editor.docInfo.id
        }
        postJson(
            '/api/publish/get_doc_info/',
            docData
        ).then(
            ({json}) => {
                this.submission = json['submission']
                this.setupUI()
            }
        ).catch(
            error => {
                addAlert('error', gettext('Could not obtain submission info.'))
                throw (error)
            }
        )

    }

    setupUI() {
        const websiteMenu = {
            title: gettext('Publish'),
            id: 'publish',
            type: 'menu',
            tooltip: gettext('Publish to website'),
            order: 10,
            disabled: editor => editor.docInfo.access_rights !== 'write',
            content: [{
                title: gettext('Submit'),
                type: 'action',
                tooltip: this.submission.user_role === 'editor' ? gettext('Publish, reject or request changes') : gettext('Submit for publishing to website'),
                action: () => {
                    if (this.submission.user_role === 'editor') {
                        this.publishDialog()
                    } else {
                        this.submitDialog()
                    }
                },
                disabled: editor => {
                    if (
                        READ_ONLY_ROLES.includes(editor.docInfo.access_rights) ||
                        COMMENT_ONLY_ROLES.includes(editor.docInfo.access_rights)
                    ) {
                        return true
                    } else {
                        return false
                    }
                }
            }]
        }
        this.editor.menu.headerbarModel.content.push(websiteMenu)
        return Promise.resolve()
    }

    submitDialog() {

        const buttons = [
            {
                text: gettext("Submit"),
                classes: "fw-dark",
                click: () => {
                    const message = document.getElementById("submission-message").value.trim()
                    this.submitDoc({message}).then(
                        () => dialog.close()
                    )
                }
            },
            {
                type: 'cancel'
            }
        ]

        const dialog = new Dialog({
            width: 750,
            buttons,
            title: gettext('Submit document to be published on website'),
            body: submitDialogTemplate({
                messages: this.submission.messages,
                status: this.submission.status
            })
        })
        dialog.open()
    }

    submitDoc({message}) {
        const docData = {
            doc_id: this.editor.docInfo.id,
            message
        }
        return postJson(
            '/api/publish/submit_doc/',
            docData
        ).then(
            ({json}) => {
                this.submission.status = json.status
                this.submission.messages.push(json.message)
                addAlert('info', gettext('Submitted document for publication.'))
            }
        )
    }

    // The dialog for a document reviewer.
    publishDialog() {
        const buttons = [
                {
                    text: gettext('Publish'),
                    click: () => {
                        const message = document.getElementById("submission-message").value.trim()
                        this.publish(message).then(
                            () => dialog.close()
                        )
                    },
                    classes: 'fw-dark'
                },
                {
                    text: gettext('Ask for changes'),
                    click: () => {
                        const message = document.getElementById("submission-message").value.trim()
                        this.review(message).then(
                            () => dialog.close()
                        )
                    },
                    classes: 'fw-dark'
                },
                {
                    text: gettext('Reject'),
                    click: () => {
                        const message = document.getElementById("submission-message").value.trim()
                        this.reject(message).then(
                            () => dialog.close()
                        )
                    },
                    classes: 'fw-dark'
                },
                {
                    type: 'cancel'
                }
            ],
            dialog = new Dialog({
                width: 750,
                id: "review-message",
                title: gettext('Publish, reject or ask for changes'),
                body: submitDialogTemplate({
                    messages: this.submission.messages,
                    status: this.submission.status
                }),
                buttons
            })

        dialog.open()
    }


    publish(message) {

        const publisher = new PublishDoc(
            this.editor.user,
            message,
            this.editor.schema,
            this.editor.app.csl,
            this.editor.mod.documentTemplate.documentStyles,
            this.editor.getDoc({changes: 'acceptAllNoInsertions'}),
            this.editor.mod.db.bibDB,
            this.editor.mod.db.imageDB,
            this.editor.docInfo.updated
        )
        return publisher.init().then(
            ({json}) => {
                this.submission.status = json.status
                this.submission.messages.push(json.message)
                addAlert('info', gettext('Published document.'))
            }
        )
    }


    reject(message) {
        return postJson(
            '/api/publish/reject_doc/',
            {
                doc_id: this.editor.docInfo.id,
                message
            }
        ).then(
            ({json}) => {
                this.submission.status = json.status
                this.submission.messages.push(json.message)
                addAlert('info', gettext('Publication of document has been rejected.'))
            }
        )
    }

    review(message) {
        return postJson(
            '/api/publish/review_doc/',
            {
                doc_id: this.editor.docInfo.id,
                message
            }
        ).then(
            ({json}) => {
                this.submission.messages.push(json.message)
                addAlert('info', gettext('Document has been reviewed. Request for changes has been sent.'))
            }
        )
    }

}
