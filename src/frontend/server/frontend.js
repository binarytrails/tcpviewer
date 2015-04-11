Meteor.startup(function () {
    var Images = new FS.Collection("images", {
        stores: [new FS.Store.FileSystem("images", {path: "~/uploads"})]
    });
    
});