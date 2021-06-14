print("Hello world")
from flask import Flask
app = Flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
    return " <html><head></head> <body> Hello World! </body></html>"
from flask import render_template
#наша новая функция сайта
# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
# модули валидации полей формы
from wtforms.validators import DataRequired
from wtforms.validators import AnyOf
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Le7_y4bAAAAAJPh53Jlz6WZOuxLoHtnmR631cao'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Le7_y4bAAAAAMTKde2Aoim2WAE_oZ2Av6QNefl7'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
# поле для введения строки, валидируется наличием данных
# валидатор проверяет введение данных после нажатия кнопки submit
# и указывает пользователю ввести данные если они не введены
# или неверны
    # поле загрузки файла
    # здесь валидатор укажет ввести правильные файлы
    upload = FileField('Load image', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    # поле формы с capture
    recaptcha = RecaptchaField()
    red = StringField('First color', validators=[DataRequired(), AnyOf(['red', 'green', 'blue'], 'red green blue only!')])
    green = StringField('Second color', validators=[DataRequired(), AnyOf(['red', 'green', 'blue'], 'red green blue only!')])
    blue = StringField('Third color', validators=[DataRequired(), AnyOf(['red', 'green', 'blue'], 'red green blue only!')])
    #кнопка submit, для пользователя отображена как send
    submit = SubmitField('send')
    # функция обработки запросов на адрес 127.0.0.1:5000/net
    # модуль проверки и преобразование имени файла
    # для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
## функция для оброботки изображения
def draw(filename,red,green,blue):
##открываем изображение
    print(filename)
    img= Image.open(filename)
    height = 224
    width = 224
    img= np.array(img.resize((height,width)))/255.0
    ##делаем график
    from skimage import io
    _ = plt.hist(img.ravel(), bins = 256, color = 'orange', )
    _ = plt.hist(img[:, :, 0].ravel(), bins = 256, color = 'Red', alpha = 0.5)
    _ = plt.hist(img[:, :, 1].ravel(), bins = 256, color = 'Green', alpha = 0.5)
    _ = plt.hist(img[:, :, 2].ravel(), bins = 256, color = 'Blue', alpha = 0.5)
    _ = plt.xlabel('Intensity Value')
    _ = plt.ylabel('Count')
    _ = plt.legend(['Total', 'Red_Channel', 'Green_Channel', 'Blue_Channel'])

    plt_img2=np.zeros((224,20,3))
    plt_img2[:,0,:]=(np.average(img,(0))).astype(np.float)
    for i in range (1,19):
        plt_img2[:,i,:]=plt_img2[:,0,:]
    plt_img2 = Image.fromarray((plt_img2 * 255).astype(np.uint8))

    plt_img=np.zeros((20,224,3))
    plt_img[0,:,:]=(np.average(img,(1))).astype(np.float)
    for i in range (1,19):
        plt_img[i,:,:]=plt_img[0,:,:]
    plt_img = Image.fromarray((plt_img * 255).astype(np.uint8))

    gr_path = "./static/newgr.png"
    plt.savefig(gr_path)
    plt.close()
    gr_path_horiz = "./static/horizgr.png"
    plt_img.save(gr_path_horiz)
    gr_path_vert = "./static/vertgr.png"
    plt_img2.save(gr_path_vert)

    result_img=np.zeros((224,224,3))
    if red == 'red':
        result_img[:,:,0] = img[:,:,0]
    if red == 'green':
        result_img[:,:,0] = img[:,:,1]
    if red == 'blue':
        result_img[:,:,0] = img[:,:,2]

    if green == 'red':
        result_img[:,:,1] = img[:,:,0]
    if green == 'green':
        result_img[:,:,1] = img[:,:,1]
    if green == 'blue':
        result_img[:,:,1] = img[:,:,2]

    if blue == 'red':
        result_img[:,:,2] = img[:,:,0]
    if blue == 'green':
        result_img[:,:,2] = img[:,:,1]
    if blue == 'blue':
        result_img[:,:,2] = img[:,:,2]
    ##сохраняем новое изображение
    result_img = Image.fromarray((result_img * 255).astype(np.uint8))
    #print(result_img)
    #img = Image.fromarray(img)
    new_path = "./static/new.png"
    img = Image.fromarray((img * 255).astype(np.uint8))
    old_path = "./static/old.png"
    img.save(old_path)
    #print(result_img)
    result_img.save(new_path)
    return new_path, gr_path, old_path, gr_path_vert, gr_path_horiz
    # метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
    # создаем объект формы
    form = NetForm(meta={'csrf': False})
    # обнуляем переменные передаваемые в форму
    filename=None
    newfilename=None
    grname=None
    oldimgname=None
    vertgr_name=None
    horizgr_name=None
    # проверяем нажатие сабмит и валидацию введенных данных
    if form.validate_on_submit():
    # файлы с изображениями читаются из каталога static
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
      #  sz=form.size.data
        red=form.red.data
        green=form.green.data
        blue=form.blue.data
        form.upload.data.save(filename)
        newfilename, grname, oldimgname, vertgr_name, horizgr_name = draw(filename,red,green,blue)
    return render_template('net.html',form=form,image_name=newfilename,gr_name=grname,old_img=oldimgname,vertgr=vertgr_name,horizgr=horizgr_name)
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
