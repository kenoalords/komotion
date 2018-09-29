var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('compilesass', function(){
    return gulp.src('./assets/*.scss')
                .pipe(sass())
                .pipe(gulp.dest('./academy/static/css'))
});

gulp.task('watch', function(){
    gulp.watch(['./assets/**/*scss'], ['compilesass']);
});
