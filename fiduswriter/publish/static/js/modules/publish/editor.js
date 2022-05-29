import {addAlert, activateWait, deactivateWait, postJson, post, Dialog} from "../common"
import {submitDialogTemplate, publishDialogTemplate} from "./templates"
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
            title: gettext('Website'),
            id: 'website',
            type: 'menu',
            tooltip: gettext('Publish to website'),
            order: 10,
            disabled: editor => editor.docInfo.access_rights !== 'write',
            content: [{
                title: this.submission.user_role === 'editor' ? gettext('Publish / Reject') : gettext('Submit'),
                type: 'action',
                tooltip: this.submission.user_role === 'editor' ? gettext('Submit publishing decision') : gettext('Submit for publishing to website'),
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
                    const messageToEditor = document.getElementById("submission-message").value.trim()
                    this.submitDoc({messageToEditor})
                    dialog.close()
                }
            },
            {
                type: 'cancel'
            }
        ]

        const dialog = new Dialog({
            height: 260,
            width: 350,
            buttons,
            title: gettext('Submit document to be published on website'),
            body: submitDialogTemplate({
                messageToEditor: this.submission.message_to_editor
            })
        })
        dialog.open()
    }

    submitDoc({messageToEditor}) {
        const docData = {
            doc_id: this.editor.docInfo.id,
            message_to_editor: messageToEditor
        }
        postJson(
            '/api/publish/submit_doc/',
            docData
        ).then(
            () => {
                this.submission.status = 'submitted'
                addAlert('info', gettext('Submitted document for publication.'))
            }
        )
    }


    publishDoc() {
        const publisher = new PublishDoc({
            doc: this.editor.getDoc(),
            imageDB: this.editor.mod.db.imageDB,
            bibDB: this.editor.mod.db.bibDB,
        })
        return publisher.init().then(
            () => {
                this.submission.status = 'published'
                addAlert('info', gettext('Published document.'))
            }
        )
    }

    // The dialog for a document reviewer.
    reviewerDialog() {
        const buttons = [
                {
                    text: gettext('Send'),
                    click: () => {
                        if (this.submitReview()) {
                            dialog.close()
                        }
                    },
                    classes: 'fw-dark'
                },
                {
                    type: 'cancel'
                }
            ],
            reviewMessageEl = document.getElementById('review-message'),
            dialog = new Dialog({
                height: 260,
                width: 350,
                id: "review-message",
                title: gettext('Leave your message for submitter'),
                body: publishDialogTemplate(),
                buttons
            })
        if (reviewMessageEl) {
            reviewMessageEl.parentElement.removeChild(reviewMessageEl)
        }

        dialog.open()
    }

    // Send the opinion of the reviewer to OJS.
    submitReview() {
        const editor_message = document.getElementById("message-editor").value,
            editor_author_message = document.getElementById("message-editor-author").value,
            recommendation = document.getElementById("recommendation").value
        if (editor_message === '' || editor_author_message === '' || recommendation === '') {
            addAlert('error', gettext('Fill out all fields before submitting!'))
            return false
        }
        activateWait()
        post(
            '/proxy/ojs/reviewer_submit',
            {
                doc_id: this.editor.docInfo.id,
                editor_message,
                editor_author_message,
                recommendation
            }
        ).then(
            () => {
                deactivateWait()
                addAlert('success', gettext('Review submitted'))
                window.setTimeout(() => window.location.reload(), 2000)
            }
        ).catch(
            error => {
                addAlert('error', gettext('Review could not be submitted.'))
                throw (error)
            }
        )
        return true
    }

}
