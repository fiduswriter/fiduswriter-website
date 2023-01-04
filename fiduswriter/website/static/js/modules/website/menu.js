export class MenuWebsite {
    constructor(menu) {
        this.menu = menu
    }

    init() {
        const documentsItem = this.menu.navItems.find(item => item.id === "documents")
        if (!documentsItem) {
            return
        }
        documentsItem.url = "/documents/"
    }
}
