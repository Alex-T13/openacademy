FROM registry.ventor.tech/docker/odoo:14.0

COPY . /addons

USER root

RUN chown -R odoo /addons
RUN sed -i /etc/odoo/odoo.conf -e '/addons_path =/s=$=,/addons=' \
    && pip3 install wheel

USER odoo
