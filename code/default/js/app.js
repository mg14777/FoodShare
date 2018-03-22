
angular.module('foodShare',['ngMaterial']).controller('foodShareController',['$http','$mdDialog',foodShareController])
.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('red')
    .accentPalette('blue');
});

var appUrl = window.location.href;//'https://bottlehello-mg14777.apaas.us2.oraclecloud.com';
var userlocation;

function foodShareController($http,$mdDialog) {
	var foodShareCtrl = this;
	foodShareCtrl.showContributeForm = function(ev) {
    $mdDialog.show({
      templateUrl: '/contribute',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true,
    })
    .then(function(contribution_succeess) {
      foodShareCtrl.status = 'The contribution was "' + contribution_succeess + '".';
    }, function() {
      foodShareCtrl.status = 'You cancelled the dialog.';
    });
  };
}
