Meteor.startup(function () {
    var fs = Npm.require('fs');
    var images = fs.readdirSync('./../../../../../public/data/');

    Images.remove({});

    _.each(_.filter(images, function(e) {
        return (e != ".DS_Store");
    }), function(e) {
       Images.insert({ name: e});
    });

});

Meteor.publish("images", function() {
    return Images.find();
});