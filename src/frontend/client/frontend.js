Meteor.subscribe("images");

Template.main.helpers({
    allImages: function() {
        return Images.find();
    }
});