
# coding: utf-8

from itertools import chain
import random
from pprint import pprint
import time
import requests


participantes = [('Ye', 'Rami'),
                 ('Lu', 'Fer'),
                 ('Juli', 'Pablo'),
                 ('Edit', 'Hora'),
                 ('Simon',)
                 ('Frida',)]

mails = {'Ye': 'yesica@test.com',
         'Rami': 'ramiro@test.com',
         'Lu': 'lu@test.com',
         'Fer': 'fer@test.com',
         'Juli': 'juli@test.com',
         'Pablo': 'pablo@test.com',
         'Edit': 'edit@test.com',
         'Hora': 'hora@test.com',
         'Simon': 'guau@test.com',
         'Frida': 'miau@test.com'}

def get_amigos(participantes):
    amigos = list()
    participantes_list = list(chain(*participantes))
    receptores = participantes_list.copy()
    
    try:
        for p in participantes_list:
            # lista reducida de receptores
            my_receptores = receptores.copy()
            # obtengo pareja
            pareja = [item for item in participantes if p in item]
            pareja = pareja[0]
          
            # pareja
            if len(pareja) == 2:
                #saco a uno mismo y la pareja
                if pareja[0] in my_receptores:
                    my_receptores.remove(pareja[0])
                if pareja[1] in my_receptores:
                    my_receptores.remove(pareja[1])
                    
            # solapa
            else:
                if pareja[0] in my_receptores:
                    my_receptores.remove(pareja[0])

            amigo = random.choice(my_receptores)

            amigos.append((p, amigo))
            receptores.remove(amigo)

    except Exception:
        amigos = get_amigos(participantes)
    return amigos

def send_mail(address, subject, html_content, text_content):
    # stdout.write(
    #     Colors.OKGREEN + '* Enviando mail a %s... ' % address + Colors.ENDC)
    mail_from_name = 'Chanta Claus'
    mail_from = 'chanta@claus.org'
    result = requests.post(
        "https://api.mailgun.net/v3/domain.com/messages",
        auth=("api", "keykeykey"),
        data={
            "from": "%s <%s>" % (mail_from_name, mail_from),
            "to": "{}".format(address),
            "subject": subject,                     
            "text": text_content,
            "html": "<html> %s </html>" % html_content
            })
                                                                                           
    return result 

# via mailgun rest api
def gen_content(amigo_a, amigo_b, id_sorteo):
    html = """<table cellspacing="0" cellpadding="0" border="0">
                <tbody><tr style="background-color:#cc0000;font-size:28px;font-family: monospace;color: #f7f7d3;padding: 10px;">
                <th style="padding: 6px 0px 0px 6px; size"><img src="http://i.imgur.com/6q2SyMA.png?1" align=left style="height: 100px; margin-left: 5px;"></th>
                <th style="padding: 10px 20px;text-align: left;">Secret Chanta App</th></tr>
                <tr style="background-color: #f7f7d3; font-size: 18px; color: #006D6A; width: 500px; padding: 10px; font-family: monospace;">
                <td colspan="2" style="padding: 20px; font-family: monospace;">
                    <p>Hola {}!</p>
                    <p style="color: #006D6A;">Tu amigo invisible es <strong>{}</strong>!</p>
                    <p>El sorteo se hace al azar (*).</p>
                    <p>Rango de regalos entre $500 y $700. No seas laucha.</p>
                    <p style="color: #006D6A;font-size: 12px">Secret Chanta App no incorpora estos datos a ningún fichero. Una vez enviados, los correos electrónicos llenarán de virus tu PC o dispositivo móvil. <br/> (*)  Cumplimos con los mismos estándares de seguridad que el voto electrónico de Cambiemos. ID de sorteo: <strong>{}</strong></p>
                </td></tr></tbody></table>""".format(amigo_a, amigo_b, id_sorteo)
    txt = """Hola {}, tu amigo invisible es {}!
             El sorteo se hace al azar. (*)
             Rango de regalos entre $500 y $700. No seas laucha.
             Secret Chanta App no incorpora estos datos a ningún fichero. Una vez enviados, los correos electrónicos llenarán de virus tu PC o dispositivo móvil. 
             Nos basamos en los mismos estándares de seguridad que el voto electrónico de Cambiemos. ID de sorteo: {}
             """.format(amigo_a, amigo_b, id_sorteo)
    return html, txt


# via smtp
def send_email(address, subject, html_content, text_content):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.headerregistry import Address
    
    mail_from_name = 'Chanta Claus'
    mail_from = 'chanta@claus.org'
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = "{} <{}>".format(mail_from_name, mail_from)
    msg['To'] = address

    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('localhost')
    s.sendmail(mail_from, address, msg.as_string())
    s.quit()

def main():
    # lista de tuplas con los pares de amigos
    amigos = get_amigos(participantes)
    id_sorteo = hex(int(time.time()))[-8:]
    amigos_list = list(chain(*participantes))

    for amigo_a in amigos_list:
        amigo_b = [item[1] for item in amigos if amigo_a == item[0]]
        amigo_b = amigo_b[0]
        html, txt = gen_content(amigo_a, amigo_b, id_sorteo)
        subject = 'Sorteo de amigo invisible!'
        print('Enviando mail a %s <%s>' % (amigo_a, mails[amigo_a]))
        send_mail(mails[amigo_a], subject, html, txt)

if __name__ == "__main__":
    main()
