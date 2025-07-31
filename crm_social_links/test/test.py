from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestPartnerSocial(TransactionCase):
    def setUp(self):
        """Preparación inicial para todas las pruebas"""
        super(TestPartnerSocial, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'facebook_url': 'https://facebook.com/valid',
            'linkedin_url': 'https://linkedin.com/in/valid',
            'twitter_url': 'https://twitter.com/valid'
        })

    def test_valid_social_urls(self):
        """Prueba la función de validación de URLs"""
        # URLs válidas
        self.assertTrue(self.partner._is_valid_social_url(
            'https://facebook.com/test', ['facebook.com']))
        # URL con dominio alternativo
        self.assertTrue(self.partner._is_valid_social_url(
            'http://fb.com/test', ['facebook.com', 'fb.com']))
        # Protocolo inválido
        self.assertFalse(self.partner._is_valid_social_url(
            'ftp://facebook.com/test', ['facebook.com']))
        # Dominio incorrecto
        self.assertFalse(self.partner._is_valid_social_url(
            'https://fake.com/test', ['facebook.com']))

    def test_compute_social_links(self):
        """Prueba la generación de iconos HTML"""
        self.partner._compute_social_links_icons()
        # Verifica que las URLs válidas generen iconos
        self.assertIn('facebook.com', self.partner.social_links_icons)
        self.assertIn('linkedin.com', self.partner.social_links_icons)
        self.assertIn('twitter.com', self.partner.social_links_icons)
        # Verifica el atributo target="_blank"
        self.assertIn('target="_blank"', self.partner.social_links_icons)

    def test_invalid_url_constraints(self):
        """Prueba que URLs inválidas generen errores"""
        with self.assertRaises(ValidationError):
            self.partner.facebook_url = 'invalid_url'
            self.partner._check_social_urls()

    def test_empty_urls(self):
        """Prueba el comportamiento con URLs vacías"""
        self.partner.write({
            'facebook_url': False,
            'linkedin_url': False,
            'twitter_url': False
        })
        self.partner._compute_social_links_icons()
        # Verifica que no se generen iconos sin URLs
        self.assertFalse(self.partner.social_links_icons)