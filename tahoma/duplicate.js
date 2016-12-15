// http://ciantic.blogspot.com/2011/09/duplicate-all-pages-in-acrobat-x.html

// First elevate privileges of the JavaScript programs:

//     Right click on document, and choose "Page Display Preferences"
//     Choose "JavaScript" from the left.
//     Check the "Enable menu items JavaScript execution privileges".

// Secondly save following snippet as duplicate.js to the /Applications/Adobe Acrobat X Pro/Adobe Acrobat Pro.app/Contents/Resources/JavaScripts folder

// quit and reopen Acrobat if "Duplicate all pages (in-place)" does not appear in the "Edit" menu

// then, use the crop pages tool twice (once on odd pages, starting with the left hand pages and then again on the even pages, on the right hand pages)  

app.addMenuItem({
        cExec: "duplicatePagesInPlace();",
        cParent: "Edit",
        cName: "Duplicate all pages (in-place)"
});

function duplicatePagesInPlace() {
    var doc = this,
        pages = this.numPages;
    for (var i = pages - 1; i >= 0; i--) {
        doc.insertPages({ 
            cPath: doc.path, 
            nStart : i, 
            nEnd : i,
            nPage : i
        });
    }
}