import {addAlert, postJson, post, Dialog} from "../common"
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
            json => {
                this.submission.status = json.status
                this.submission.message_to_editor = messageToEditor
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
                        if (this.publish()) {
                            dialog.close()
                        }
                    },
                    classes: 'fw-dark'
                },
                {
                    text: gettext('Reject'),
                    click: () => {
                        if (this.reject()) {
                            dialog.close()
                        }
                    },
                    classes: 'fw-dark'
                },
                {
                    type: 'cancel'
                }
            ],
            dialog = new Dialog({
                height: 260,
                width: 350,
                id: "review-message",
                title: gettext('Publish or reject'),
                body: publishDialogTemplate({
                    messageToEditor: this.submission.message_to_editor
                }),
                buttons
            })

        dialog.open()
    }


    publish() {
        const publisher = new PublishDoc(
            this.editor.schema,
            this.editor.app.csl,
            this.editor.mod.documentTemplate.documentStyles,
            this.editor.getDoc({changes: 'acceptAllNoInsertions'}),
            this.editor.mod.db.bibDB,
            this.editor.mod.db.imageDB,
            this.editor.docInfo.updated
        )
        return publisher.init().then(
            () => {
                this.submission.status = 'published'
                this.submission.message_to_editor = ""
                addAlert('info', gettext('Published document.'))
            }
        )
    }


    reject() {
        post(
            '/api/publish/reject_doc/'
        ).then(
            () => {
                this.submission.status = "unsubmitted"
                this.submission.message_to_editor = ""
                addAlert('info', gettext('Publication of document has been rejected.'))
            }
        )
    }

}
