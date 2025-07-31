from odoo import models, fields, api
from urllib.parse import urlparse
from odoo.exceptions import ValidationError
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'

    facebook_url = fields.Char(string='Facebook URL', help='URL completa del perfil de Facebook')    
    linkedin_url = fields.Char(string='LinkedIn URL', help='URL completa del perfil de LinkedIn')    
    twitter_url = fields.Char(string='Twitter URL', help='URL completa del perfil de Twitter')    
    # Campo computado para mostrar iconos en la vista lista
    social_links_icons = fields.Html(string='Redes Sociales', compute='_compute_social_links_icons', sanitize=False)
    social_status = fields.Selection(selection=[
            ('incomplete', 'Incompleto'),
            ('partial', 'Parcial'),
            ('complete', 'Completo'),
        ],
        string='Estado Redes Sociales',
        compute='_compute_social_status',
        store=True,
        default='incomplete'
    )
    
    
    @api.depends('facebook_url', 'linkedin_url', 'twitter_url')
    def _compute_social_links_icons(self):
        social_config = {
            'facebook': {
                'icon': 'fa-facebook-square',
                'color': '#3b5998',
                'domains': ['facebook.com', 'fb.com']
            },
            'linkedin': {
                'icon': 'fa-linkedin-square',
                'color': '#0077b5',
                'domains': ['linkedin.com', 'www.linkedin.com']
            },
            'twitter': {
                'icon': 'fa-twitter-square',
                'color': '#1da1f2',
                'domains': ['twitter.com', 'x.com']
            }
        }
        
        for partner in self:
            html_links = []
            for field_name, config in social_config.items():
                url = getattr(partner, f"{field_name}_url")
                if url and partner._is_valid_social_url(url, config['domains']):
                    html_links.append(
                        f'<a href="{url}" target="_blank" title="Ir a {field_name.capitalize()}" '
                        f'style="color: {config["color"]}; margin-right: 10px; font-size: 1.5em;">'
                        f'<i class="fa {config["icon"]}"></i></a>'
                    )
            
            partner.social_links_icons = ''.join(html_links) if html_links else False
    @api.constrains('facebook_url', 'linkedin_url', 'twitter_url')
    def _check_social_urls(self):
        for partner in self:
            # Validación para Facebook
            if partner.facebook_url:
                self._validate_social_network_url(
                    url=partner.facebook_url,
                    network_name='Facebook',
                    valid_domains=['facebook.com', 'fb.com'],
                    path_regex=r'^\/[^\/]+\/?$',  # Ej: /nombreusuario
                    allow_query_params=False
                )
            
            # Validación para LinkedIn
            if partner.linkedin_url:
                self._validate_social_network_url(
                    url=partner.linkedin_url,
                    network_name='LinkedIn',
                    valid_domains=['linkedin.com', 'linked.in'],
                    path_regex=r'^\/in\/[^\/]+\/?$',  # Ej: /in/nombreusuario
                    allow_query_params=True
                )
            
            # Validación para Twitter/X
            if partner.twitter_url:
                self._validate_social_network_url(
                    url=partner.twitter_url,
                    network_name='Twitter/X',
                    valid_domains=['twitter.com', 'x.com'],
                    path_regex=r'^\/[^\/]+\/?$',  # Ej: /nombreusuario
                    allow_query_params=False
                )
    
    def _validate_social_network_url(self, url, network_name, valid_domains, path_regex=None, allow_query_params=True):
        """ Método genérico para validar URLs de redes sociales """
        try:
            parsed = urlparse(url)
            
            # 1. Validar esquema (https)
            if not parsed.scheme or parsed.scheme not in ('http', 'https'):
                raise ValidationError(
                    f"La URL de {network_name} debe comenzar con http:// o https://"
                )
                
            # 2. Validar dominio
            domain_valid = any(domain in parsed.netloc for domain in valid_domains)
            if not domain_valid:
                raise ValidationError(
                    f"La URL de {network_name} debe contener uno de estos dominios: {', '.join(valid_domains)}"
                )
                
            # 3. Validar estructura del path
            if path_regex and not re.match(path_regex, parsed.path):
                raise ValidationError(
                    f"La URL de {network_name} no tiene el formato correcto. Ejemplo válido: https://{valid_domains[0]}/nombredeusuario"
                )
                
            # 4. Validar parámetros de consulta
            if not allow_query_params and parsed.query:
                raise ValidationError(
                    f"La URL de {network_name} no debe contener parámetros de consulta (?...) "
                )
                
            # 5. Validar caracteres especiales
            if re.search(r'[^\w\-\.\/\:]', url):
                raise ValidationError(
                    f"La URL de {network_name} contiene caracteres inválidos"
                )
                
        except ValueError as e:
            raise ValidationError(f"URL de {network_name} inválida: {str(e)}")  
    
    
    @api.depends('facebook_url', 'linkedin_url', 'twitter_url')
    def _compute_social_status(self):
        for partner in self:
            urls = [partner.facebook_url, partner.linkedin_url, partner.twitter_url]
            filled = [bool(url) for url in urls]
            count = sum(filled)

            if count == 3:
                partner.social_status = 'complete'
            elif count == 0:
                partner.social_status = 'incomplete'
            else:
                partner.social_status = 'partial'


    def _is_valid_social_url(self, url, valid_domains):
        """Valida URLs de redes sociales"""
        if not url:
            return False
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return False
            return any(domain in parsed.netloc.lower() for domain in valid_domains)
        except Exception:
            return False
    
    def _get_social_links(self):
        """Retorna diccionario con links válidos"""
        self.ensure_one()
        social_links = {}
        
        if self._is_valid_social_url(self.facebook_url, ['facebook.com', 'fb.com']):
            social_links['facebook'] = {
                'url': self.facebook_url,
                'icon': 'fa-facebook',
                'color': '#3b5998'
            }
            
        if self._is_valid_social_url(self.linkedin_url, ['linkedin.com']):
            social_links['linkedin'] = {
                'url': self.linkedin_url,
                'icon': 'fa-linkedin',
                'color': '#0077b5'
            }
            
        if self._is_valid_social_url(self.twitter_url, ['twitter.com', 'x.com']):
            social_links['twitter'] = {
                'url': self.twitter_url,
                'icon': 'fa-twitter',
                'color': '#1da1f2'
            }
            
        return social_links

    