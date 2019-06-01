from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Post
from flask_login import login_required
from flask_uploads import UploadSet, configure_uploads, IMAGES
from . import get_query_images
from werkzeug import utils
import boto3
from app import S3_BUCKET, S3_KEY, S3_SECRET
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def _get_s3_resource():
    if S3_KEY and S3_SECRET:
        return boto3.resource(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )
    else:
        return boto3.resource('s3')


def _get_s3_client():
    if S3_KEY and S3_SECRET:
        return boto3.client(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )
    else:
        return boto3.client('s3')


def get_bucket():
    s3_resource = _get_s3_resource()
    return s3_resource.Bucket(S3_BUCKET)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('upload', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            if user is not None:
                app.logger.info('%s FAILED TO LOG IN', user.username)
            else:
                app.logger.info('USER FAILED TO LOG IN')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        app.logger.info('%s SUCCESSFULLY LOGGED IN', user.username)
        return redirect(url_for('upload', username=user.username))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    app.logger.info('User was logged out')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('upload', username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            app.logger.info('NEW USER %s SUCCESSFULLY REGISTERED', user.username)
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/upload/<username>', methods=['POST', 'GET'])
@login_required
def upload(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.username != current_user.username:
        return redirect(url_for('upload', username=current_user.username))
    app.config['UPLOADED_PHOTOS_DEST'] = user.username + "/"
    bucket = get_bucket()
    file = UploadSet('photos', IMAGES)
    configure_uploads(app, file)
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = utils.secure_filename(file.filename)
            path = user.username + "/" + filename
            bucket.Object(path).put(Body=file)
            if not check_if_exist(path):
                p = Post(body=path, author=user)
                db.session.add(p)
                db.session.commit()

            app.logger.info('%s SUCCESSFULLY UPLOADED PHOTO', user.username)
            s3 = _get_s3_client()
            filepath = s3.generate_presigned_url('get_object',
                                                 Params={'Bucket': S3_BUCKET,
                                                         'Key': path},
                                                 ExpiresIn=200)
            item_list = get_query_images.get_query_images(filepath)
            mock_list = []
            for item in item_list:
                url = s3.generate_presigned_url('get_object',
                                                Params={'Bucket': S3_BUCKET,
                                                        'Key': item},
                                                ExpiresIn=200)
                mock_list.append(url)

            mock_list = zip(mock_list, item_list)
            return render_template('display.html',
                                   filepath=filepath,
                                   mock=mock_list,
                                   query_name=filename)

        app.logger.info('%s ATTEMPTED TO UPLOAD INCOMPATIBLE FILE TYPE', user.username)
        flash('Incompatible File. Accepted file types are {}'.format(
            ALLOWED_EXTENSIONS))
    return render_template('index.html')


@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']
    bucket = get_bucket()
    q = db.session.query(Post).filter(Post.body == key)
    q.delete()
    db.session.commit()
    bucket.Object(key).delete()
    app.logger.info('%s deleted file %s', current_user.username, key)
    flash('Successfully removed file {}'.format(key))
    return redirect(url_for('user', username=current_user.username))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.username != current_user.username:
        return redirect(url_for('user', username=current_user.username))
    posts = user.posts
    bucket = get_bucket()
    key = user.username+"/"
    objs = list(bucket.objects.filter(Prefix=key))
    signed_urls = []
    s3 = _get_s3_client()
    for post in posts:
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': S3_BUCKET,
                                                'Key': post.body},
                                        ExpiresIn=100)
        signed_urls.append(url)
    summaries = zip(objs, signed_urls)
    return render_template('user.html', user=user, files=summaries)


@app.route('/search_previous', methods=['POST'])
def search_previous():
    key = request.form['key']
    s3 = _get_s3_client()
    filepath = s3.generate_presigned_url('get_object',
                                         Params={'Bucket': S3_BUCKET,
                                                 'Key': key},
                                         ExpiresIn=200)
    item_list = get_query_images.get_query_images(filepath)
    mock_list = []
    for item in item_list:
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': S3_BUCKET,
                                                'Key': item},
                                        ExpiresIn=200)
        mock_list.append(url)

    mock_list = zip(mock_list, item_list)
    return render_template('display.html',
                           filepath=filepath,
                           mock=mock_list,
                           query_name=key.split('/')[-1])


@app.route('/delete_account')
def del_account():
    user = db.session.query(User).filter(User.username == current_user.username)
    user.delete()
    bucket = get_bucket()
    posts = Post.query.all()
    for post in posts:
        db.session.delete(post)
    bucket.objects.filter(Prefix=current_user.username+'/').delete()
    app.logger.info('%s DELETED ACCOUNT', current_user.username)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/ratings', methods=['GET', 'POST'])
def ratings():
    key = request.form['key'].replace("'", "").replace("(", "").replace(")", "")\
        .replace('[', "").replace(']', "").split(',')
    s3 = boto3.resource('s3')
    query_key = current_user.username+'/' + key[0]
    print(query_key)
    copy_source = {
        'Bucket': 'simsearch',
        'Key': query_key
    }
    s3.meta.client.copy(copy_source, 'simsearch', 'results/' +
                        query_key + '/'+key[0])

    result_key = key[1].replace(']', "").strip()
    rating_res = key[2].replace(']', "").strip()
    copy_source = {
        'Bucket': 'simsearch',
        'Key': result_key
    }
    name = result_key.split('/')[-2] + result_key.split('/')[-1]
    print('results/' + query_key + '/'
          + rating_res+'/' + name)
    s3.meta.client.copy(copy_source, 'simsearch', 'results/' + query_key +
                        '/'+rating_res+'/' + name)

    s3 = _get_s3_client()
    filepath = s3.generate_presigned_url('get_object',
                                         Params={'Bucket': S3_BUCKET,
                                                 'Key': query_key},
                                         ExpiresIn=200)
    item_list = get_query_images.get_query_images(filepath)
    mock_list = []
    for item in item_list:
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': S3_BUCKET,
                                                'Key': item},
                                        ExpiresIn=200)
        mock_list.append(url)

    mock_list = zip(mock_list, item_list)
    app.logger.info('%s RATED AN IMAGE', current_user.username)
    flash('Thank you for your feedback!')
    return render_template('display.html',
                           filepath=filepath,
                           mock=mock_list,
                           query_name=key)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_if_exist(filename):
    q = db.session.query(Post).filter(Post.body == filename)
    if q.all():
        return True
    return False
