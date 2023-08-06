'use strict';

angular.module('ajenti.filesystem', ['core', 'angularFileUpload']);
'use strict';

angular.module('ajenti.filesystem').controller('DiskWidgetController', function ($scope) {
    return $scope.$on('widget-update', function ($event, id, data) {
        if (id !== $scope.widget.id) {
            return;
        }
        return $scope.service = data;
    });
});

angular.module('ajenti.filesystem').controller('DiskWidgetConfigController', function ($scope, filesystem) {
    $scope.services = [];

    return filesystem.mountpoints().then(function (data) {
        return $scope.mountpoints = data;
    });
});
'use strict';

angular.module('ajenti.filesystem').directive('fileDialog', function ($timeout, filesystem, notify, hotkeys, identity, gettext) {
    return {
        scope: {
            ngShow: "=?",
            onSelect: "&",
            onCancel: "&?",
            root: '=?',
            mode: '@?',
            name: '=?',
            path: '=?'
        },
        templateUrl: '/filesystem:resources/js/directives/fileDialog.html',
        link: function link($scope, element, attrs) {
            element.addClass('block-element');
            $scope.loading = false;
            if ($scope.mode == null) {
                $scope.mode = 'open';
            }
            if ($scope.path == null) {
                $scope.path = '/';
            }

            $scope.navigate = function (path, explicit) {
                $scope.loading = true;
                return filesystem.list(path).then(function (data) {
                    $scope.loadedPath = path;
                    $scope.path = path;
                    $scope.items = data.items;
                    $scope.parent = data.parent;
                    if ($scope.path === $scope.root) {
                        $scope.parent = null;
                    } else if ($scope.path.indexOf($scope.root) !== 0) {
                        $scope.navigate($scope.root);
                    }
                    return $scope.restoreFocus();
                }).catch(function (data) {
                    if (explicit) {
                        return notify.error(gettext('Could not load directory'), data.message);
                    }
                }).finally(function () {
                    return $scope.loading = false;
                });
            };

            $scope.select = function (item) {
                if (item.isDir) {
                    return $scope.navigate(item.path, true);
                } else {
                    if ($scope.mode === 'open') {
                        $scope.onSelect({ path: item.path });
                    }
                    if ($scope.mode === 'save') {
                        return $scope.name = item.name;
                    }
                }
            };

            $scope.save = function () {
                return $scope.onSelect({ path: $scope.path + '/' + $scope.name });
            };

            $scope.selectDirectory = function () {
                return $scope.onSelect({ path: $scope.path });
            };

            hotkeys.on($scope, function (char) {
                if ($scope.ngShow && char === hotkeys.ESC) {
                    $scope.onCancel();
                    return true;
                }
            });

            $scope.restoreFocus = function () {
                return setTimeout(function () {
                    return element.find('.list-group a').first().blur().focus();
                });
            };

            return identity.promise.then(function () {
                if ($scope.root == null) {
                    $scope.root = identity.profile.fs_root || '/';
                }

                $scope.$watch('ngShow', function () {
                    if ($scope.ngShow) {
                        return $scope.restoreFocus();
                    }
                });

                $scope.$watch('root', function () {
                    return $scope.navigate($scope.root);
                });

                return $scope.$watch('path', function () {
                    if ($scope.loadedPath !== $scope.path) {
                        return $scope.navigate($scope.path);
                    }
                });
            });
        }
    };
});
'use strict';

angular.module('ajenti.filesystem').directive('pathSelector', function () {
    return {
        restrict: 'E',
        scope: {
            ngModel: '=',
            mode: '@'
        },
        template: '<div>\n    <div class="input-group">\n        <input ng:model="ngModel" type="text" class="form-control" ng:required="attr.required" />\n        <span class="input-group-addon">\n            <a ng:click="openDialogVisible = true"><i class="fa fa-folder-open"></i></a>\n        </span>\n    </div>\n    <file-dialog\n        mode="{{mode}}"\n        path="path"\n        ng:show="openDialogVisible"\n        on-select="select(path)"\n        on-cancel="openDialogVisible = false" />\n</div>',
        link: function link($scope, element, attr, ctrl) {
            $scope.attr = attr;
            $scope.path = '/';
            if ($scope.mode == null) {
                $scope.mode = 'open';
            }

            $scope.select = function (path) {
                $scope.ngModel = path;
                return $scope.openDialogVisible = false;
            };

            return $scope.$watch('ngModel', function () {
                if ($scope.ngModel) {
                    if ($scope.mode === 'directory') {
                        return $scope.path = $scope.ngModel;
                    } else {
                        return $scope.path = $scope.ngModel.substr(0, $scope.ngModel.lastIndexOf('/'));
                    }
                }
            });
        }
    };
});
'use strict';

angular.module('ajenti.filesystem').service('filesystem', function ($http, $q) {
    this.mountpoints = function () {
        var q = $q.defer();
        $http.get("/api/filesystem/mountpoints").success(function (data) {
            return q.resolve(data);
        }).error(function (err) {
            return q.reject(err);
        });
        return q.promise;
    };

    this.read = function (path, encoding) {
        var q = $q.defer();
        $http.get('/api/filesystem/read/' + path + '?encoding=' + (encoding || 'utf-8')).success(function (data) {
            return q.resolve(data);
        }).error(function (err) {
            return q.reject(err);
        });
        return q.promise;
    };

    this.write = function (path, content, encoding) {
        var q = $q.defer();
        $http.post('/api/filesystem/write/' + path + '?encoding=' + (encoding || 'utf-8'), content).success(function (data) {
            return q.resolve(data);
        }).error(function (err) {
            return q.reject(err);
        });
        return q.promise;
    };

    this.list = function (path) {
        var q = $q.defer();
        $http.get('/api/filesystem/list/' + path).success(function (data) {
            return q.resolve(data);
        }).error(function (err) {
            return q.reject(err);
        });
        return q.promise;
    };

    this.stat = function (path) {
        var q = $q.defer();
        $http.get('/api/filesystem/stat/' + path).success(function (data) {
            return q.resolve(data);
        }).error(function (err) {
            return q.reject(err);
        });
        return q.promise;
    };

    this.chmod = function (path, mode) {
        var q = $q.defer();
        $http.post('/api/filesystem/chmod/' + path, { mode: mode }).success(function (data) {
            return q.resolve(data);
        }).error(function (err) {
            return q.reject(err);
        });
        return q.promise;
    };

    this.createFile = function (path, mode) {
        var q = $q.defer();
        $http.post('/api/filesystem/create-file/' + path, { mode: mode }).success(function (data) {
            return q.resolve(data);
        }).error(function (err) {
            return q.reject(err);
        });
        return q.promise;
    };

    this.createDirectory = function (path, mode) {
        var q = $q.defer();
        $http.post('/api/filesystem/create-directory/' + path, { mode: mode }).success(function (data) {
            return q.resolve(data);
        }).error(function (err) {
            return q.reject(err);
        });
        return q.promise;
    };

    this.downloadBlob = function (content, mime, name) {
        return setTimeout(function () {
            var blob = new Blob([content], { type: mime });
            var elem = window.document.createElement('a');
            elem.href = URL.createObjectURL(blob);
            elem.download = name;
            document.body.appendChild(elem);
            elem.click();
            return document.body.removeChild(elem);
        });
    };

    return this;
});