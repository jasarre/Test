# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class medical_patient(models.Model):
    
    _name = 'medical.patient'
    _description = 'medical patient'
    _rec_name = 'patient_id'

    #Agregar pdf en Consentimientos
    consent_pdf = fields.Many2many(
        comodel_name='ir.attachment',
        relation='patient_consent_image_rel',
        column1='patient_id',
        column2='attachment_id',
        string="Añadir archivo"
    )

    #Funcinalidad botón Consentimientos para ir a firmas
    def action_consentimiento(self):  
        return {
            'res_model': 'sign.template',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("sign.sign_template_view_kanban").id,
            'target': 'self'
        }



    @api.onchange('patient_id')
    def _onchange_patient(self):
        '''
        The purpose of the method is to define a domain for the available
        purchase orders.
        '''
        address_id = self.patient_id
        self.partner_address_id = address_id

    def print_report(self):
        return self.env.ref('basic_hms.report_print_patient_card').report_action(self)

    @api.depends('date_of_birth')
    def onchange_age(self):
        for rec in self:
            if rec.date_of_birth:
                d1 = rec.date_of_birth
                d2 = datetime.today().date()
                rd = relativedelta(d2, d1)
                rec.age = str(rd.years) + "y" +" "+ str(rd.months) + "m" +" "+ str(rd.days) + "d"
            else:
                rec.age = "No Date Of Birth!!"

    patient_id = fields.Many2one('res.partner',domain=[('is_patient','=',True)],string="Patient", required= True)
    name = fields.Char(string='Id', readonly=True)
    last_name = fields.Char('Last name')
    
    # AÑADO CAMPOS RELACIONADOS DE CONTACTOS:VAT, PHONE, MOBILE, EMAIL
    partner_vat = fields.Char(related='patient_id.vat', string='NIF', readonly=True)
    partner_phone = fields.Char(related='patient_id.phone', string='Phone', readonly=True)
    partner_mobile = fields.Char(related='patient_id.mobile', string='Mobile', readonly=True)
    partner_email = fields.Char(related='patient_id.email', string='Email', readonly=True)

    #AÑADO CAMPOS QUE INCORPOO A LA VISTA DE PACIENTES
    nuhsa = fields.Char(string="NUHSA")
    nuss = fields.Integer(string="NUSS")

    
    date_of_birth = fields.Date(string="Date of Birth")
    sex = fields.Selection([('m', 'Male'),('f', 'Female')], string ="Sex")
    age = fields.Char(compute=onchange_age,string="Patient Age",store=True)
    critical_info = fields.Text(string="Patient Critical Information")
    photo = fields.Binary(string="Picture")
    blood_type = fields.Selection([('A', 'A'),('B', 'B'),('AB', 'AB'),('O', 'O')], string ="Blood Type")
    rh = fields.Selection([('-+', '+'),('--', '-')], string ="Rh")
    marital_status = fields.Selection([('s','Single'),('m','Married'),('w','Widowed'),('d','Divorced'),('x','Seperated')],string='Marital Status')
    deceased = fields.Boolean(string='Deceased')
    date_of_death = fields.Date(string="Date of Death")
    cause_of_death = fields.Char(string='Cause of Death')
    receivable = fields.Float(string="Receivable", readonly=True)
    current_insurance_id = fields.Many2one('medical.insurance',string="Insurance")
    partner_address_id = fields.Many2one('res.partner', string="Address", )

    street = fields.Char(related='patient_id.street', readonly=False)
    street2 = fields.Char(related='patient_id.street2', readonly=False)
    zip_code = fields.Char(related='patient_id.zip', readonly=False)
    city = fields.Char(related='patient_id.city', readonly=False)
    state_id = fields.Many2one("res.country.state", related='patient_id.state_id', readonly=False)
    country_id = fields.Many2one('res.country', related='patient_id.country_id', readonly=False)
    
    primary_care_physician_id = fields.Many2one('medical.physician', string="Primary Care Doctor")
    patient_status = fields.Char(string="Hospitalization Status",readonly=True)
    patient_disease_ids = fields.One2many('medical.patient.disease','patient_id')
    patient_psc_ids = fields.One2many('medical.patient.psc','patient_id')
    excercise = fields.Boolean(string='Excercise')
    excercise_minutes_day = fields.Integer(string="Minutes/Day")
    sleep_hours = fields.Integer(string="Hours of sleep")
    sleep_during_daytime = fields.Boolean(string="Sleep at daytime")
    number_of_meals = fields.Integer(string="Meals per day")
    coffee = fields.Boolean('Coffee')
    coffee_cups = fields.Integer(string='Cups Per Day')
    eats_alone = fields.Boolean(string="Eats alone")
    soft_drinks = fields.Boolean(string="Soft drinks(sugar)")
    salt = fields.Boolean(string="Salt")
    diet = fields.Boolean(string=" Currently on a diet ")
    diet_info = fields.Integer(string=' Diet info ')
    general_info = fields.Text(string="Info")
    lifestyle_info = fields.Text('Lifestyle Information')
    smoking = fields.Boolean(string="Smokes")
    smoking_number = fields.Integer(string="Cigarretes a day")
    ex_smoker = fields.Boolean(string="Ex-smoker")
    second_hand_smoker = fields.Boolean(string="Passive smoker")
    age_start_smoking = fields.Integer(string="Age started to smoke")
    age_quit_smoking = fields.Integer(string="Age of quitting")
    drug_usage = fields.Boolean(string='Drug Habits')
    drug_iv = fields.Boolean(string='IV drug user')
    ex_drug_addict = fields.Boolean(string='Ex drug addict')
    age_start_drugs = fields.Integer(string='Age started drugs')
    age_quit_drugs = fields.Integer(string="Age quit drugs")
    alcohol = fields.Boolean(string="Drinks Alcohol")
    ex_alcohol = fields.Boolean(string="Ex alcoholic")
    age_start_drinking = fields.Integer(string="Age started to drink")
    age_quit_drinking = fields.Integer(string="Age quit drinking")
    alcohol_beer_number = fields.Integer(string="Beer / day")
    alcohol_wine_number = fields.Integer(string="Wine / day")
    alcohol_liquor_number = fields.Integer(string="Liquor / day")
    cage_ids = fields.One2many('medical.patient.cage','patient_id')
    sex_oral = fields.Selection([('0','None'),
                                 ('1','Active'),
                                 ('2','Passive'),
                                 ('3','Both')],string='Oral Sex')
    sex_anal = fields.Selection([('0','None'),
                                 ('1','Active'),
                                 ('2','Passive'),
                                 ('3','Both')],string='Anal Sex')
    prostitute = fields.Boolean(string='Prostitute')
    sex_with_prostitutes = fields.Boolean(string=' Sex with prostitutes ')
    sexual_preferences = fields.Selection([
            ('h', 'Heterosexual'),
            ('g', 'Homosexual'),
            ('b', 'Bisexual'),
            ('t', 'Transexual'),
        ], 'Sexual Orientation', sort=False)
    sexual_practices = fields.Selection([
            ('s', 'Safe / Protected sex'),
            ('r', 'Risky / Unprotected sex'),
        ], 'Sexual Practices', sort=False)
    sexual_partners = fields.Selection([
            ('m', 'Monogamous'),
            ('t', 'Polygamous'),
        ], 'Sexual Partners', sort=False)
    sexual_partners_number = fields.Integer('Number of sexual partners')
    first_sexual_encounter = fields.Integer('Age first sexual encounter')
    anticonceptive = fields.Selection([
            ('0', 'None'),
            ('1', 'Pill / Minipill'),
            ('2', 'Male condom'),
            ('3', 'Vasectomy'),
            ('4', 'Female sterilisation'),
            ('5', 'Intra-uterine device'),
            ('6', 'Withdrawal method'),
            ('7', 'Fertility cycle awareness'),
            ('8', 'Contraceptive injection'),
            ('9', 'Skin Patch'),
            ('10', 'Female condom'),
        ], 'Anticonceptive Method', sort=False)
    sexuality_info = fields.Text('Extra Information')
    motorcycle_rider = fields.Boolean('Motorcycle Rider', help="The patient rides motorcycles")
    helmet = fields.Boolean('Uses helmet', help="The patient uses the proper motorcycle helmet")
    traffic_laws = fields.Boolean('Obeys Traffic Laws', help="Check if the patient is a safe driver")
    car_revision = fields.Boolean('Car Revision', help="Maintain the vehicle. Do periodical checks - tires,breaks ...")
    car_seat_belt = fields.Boolean('Seat belt', help="Safety measures when driving : safety belt")
    car_child_safety = fields.Boolean('Car Child Safety', help="Safety measures when driving : child seats, proper seat belting, not seating on the front seat, ....")
    home_safety = fields.Boolean('Home safety', help="Keep safety measures for kids in the kitchen, correct storage of chemicals, ...")
    fertile = fields.Boolean('Fertile')
    menarche = fields.Integer('Menarche Age')
    menopausal = fields.Boolean('Menopausal')
    menopause = fields.Integer('Menopause age')
    menstrual_history_ids = fields.One2many('medical.patient.menstrual.history','patient_id')
    breast_self_examination = fields.Boolean('Breast self-examination')
    mammography = fields.Boolean('Mammography')
    pap_test = fields.Boolean('PAP test')
    last_pap_test = fields.Date('Last PAP test')
    colposcopy = fields.Boolean('Colposcopy')
    mammography_history_ids = fields.One2many('medical.patient.mammography.history','patient_id')
    pap_history_ids = fields.One2many('medical.patient.pap.history','patient_id')
    colposcopy_history_ids = fields.One2many('medical.patient.colposcopy.history','patient_id')
    pregnancies = fields.Integer('Pregnancies')
    premature = fields.Integer('Premature')
    stillbirths = fields.Integer('Stillbirths')
    abortions = fields.Integer('Abortions')
    pregnancy_history_ids = fields.One2many('medical.patient.pregnency','patient_id')
    family_history_ids = fields.Many2many('medical.family.disease',string="Family Disease Lines")
    perinatal_ids = fields.Many2many('medical.preinatal')
    ex_alcoholic = fields.Boolean('Ex Alcoholic')
    currently_pregnant = fields.Boolean('Currently Pregnant')
    born_alive = fields.Integer('Born Alive')
    gpa = fields.Char('GPA')
    works_at_home = fields.Boolean('Works At Home')
    colposcopy_last = fields.Date('Last colposcopy')
    mammography_last = fields.Date('Last mammography')
    ses = fields.Selection([
            ('None', ''),
            ('0', 'Lower'),
            ('1', 'Lower-middle'),
            ('2', 'Middle'),
            ('3', 'Middle-upper'),
            ('4', 'Higher'),
        ], 'Socioeconomics', help="SES - Socioeconomic Status", sort=False)
    education = fields.Selection([('o','None'),('1','Incomplete Primary School'),
                                  ('2','Primary School'),
                                  ('3','Incomplete Secondary School'),
                                  ('4','Secondary School'),
                                  ('5','University')],string='Education Level')
    housing = fields.Selection([
            ('None', ''),
            ('0', 'Shanty, deficient sanitary conditions'),
            ('1', 'Small, crowded but with good sanitary conditions'),
            ('2', 'Comfortable and good sanitary conditions'),
            ('3', 'Roomy and excellent sanitary conditions'),
            ('4', 'Luxury and excellent sanitary conditions'),
        ], 'Housing conditions', help="Housing and sanitary living conditions", sort=False)
    works = fields.Boolean('Works')
    hours_outside = fields.Integer('Hours outside home', help="Number of hours a day the patient spend outside the house")
    hostile_area = fields.Boolean('Hostile Area')
    notes = fields.Text(string="Extra info")
    sewers = fields.Boolean('Sanitary Sewers')
    water = fields.Boolean('Running Water')
    trash = fields.Boolean('Trash recollection')
    electricity = fields.Boolean('Electrical supply')
    gas = fields.Boolean('Gas supply')
    telephone = fields.Boolean('Telephone')
    television = fields.Boolean('Television')
    internet = fields.Boolean('Internet')
    single_parent= fields.Boolean('Single parent family')
    domestic_violence = fields.Boolean('Domestic violence')
    working_children = fields.Boolean('Working children')
    teenage_pregnancy = fields.Boolean('Teenage pregnancy')
    sexual_abuse = fields.Boolean('Sexual abuse')
    drug_addiction = fields.Boolean('Drug addiction')
    school_withdrawal = fields.Boolean('School withdrawal')
    prison_past = fields.Boolean('Has been in prison')
    prison_current = fields.Boolean('Is currently in prison')
    relative_in_prison = fields.Boolean('Relative in prison', help="Check if someone from the nuclear family - parents sibblings  is or has been in prison")
    fam_apgar_help = fields.Selection([
            ('None', ''),
            ('0', 'None'),
            ('1', 'Moderately'),
            ('2', 'Very much'),
        ], 'Help from family',
            help="Is the patient satisfied with the level of help coming from the family when there is a problem ?", sort=False)
    fam_apgar_discussion = fields.Selection([
            ('None', ''),
            ('0', 'None'),
            ('1', 'Moderately'),
            ('2', 'Very much'),
        ], 'Problems discussion',
            help="Is the patient satisfied with the level talking over the problems as family ?", sort=False)
    fam_apgar_decisions = fields.Selection([
            ('None', ''),
            ('0', 'None'),
            ('1', 'Moderately'),
            ('2', 'Very much'),
        ], 'Decision making',
            help="Is the patient satisfied with the level of making important decisions as a group ?", sort=False)
    fam_apgar_timesharing = fields.Selection([
            ('None', ''),
            ('0', 'None'),
            ('1', 'Moderately'),
            ('2', 'Very much'),
        ], 'Time sharing',
            help="Is the patient satisfied with the level of time that they spend together ?", sort=False)
    fam_apgar_affection = fields.Selection([
            ('None', ''),
            ('0', 'None'),
            ('1', 'Moderately'),
            ('2', 'Very much'),
        ], 'Family affection',
            help="Is the patient satisfied with the level of affection coming from the family ?", sort=False)
    fam_apgar_score = fields.Integer('Score', help="Total Family APGAR 7 - 10 : Functional Family 4 - 6  : Some level of disfunction \n"
                                          "0 - 3  : Severe disfunctional family \n")
    lab_test_ids = fields.One2many('medical.patient.lab.test','patient_id')
    fertile = fields.Boolean('Fertile')
    menarche_age  = fields.Integer('Menarche age')
    menopausal = fields.Boolean('Menopausal')
    pap_test_last = fields.Date('Last PAP Test')
    colposcopy = fields.Boolean('Colpscopy')
    gravida = fields.Integer('Pregnancy')
    medical_vaccination_ids = fields.One2many('medical.vaccination','medical_patient_vaccines_id')
    medical_appointments_ids = fields.One2many('medical.appointment','patient_id',string='Appointments')
    lastname = fields.Char('Last Name')
    report_date = fields.Date('Date',default = datetime.today().date())
    medication_ids = fields.One2many('medical.patient.medication1','medical_patient_medication_id')
    deaths_2nd_week = fields.Integer('Deceased after 2nd week')
    deaths_1st_week = fields.Integer('Deceased after 1st week')
    full_term = fields.Integer('Full Term')
    ses_notes = fields.Text('Notes')

    #AÑADO CAMPOS PARA MODIFICACIÓN DE LA SOLAPA ESTILO DE VIDA->DIETA Y EJERCICIO
    breackfast = fields.Char(string='Desayuno')
    lunch = fields.Char(string='Almuerzo')
    dinner = fields.Char(string='Cena')
    midmorning = fields.Char(string='Media mañana')
    snack = fields.Char(string='Merienda')
    water_per_day = fields.Integer(string='Litros de agua al día')
    comment_habitos_alimentarios = fields.Text(string="Comentario sobre hábitos alimentarios")
    bowel_habit = fields.Boolean(string='Hábito intestinal controlado')
    bowel_habit_comment = fields.Char(string='Comentario hábito instestinal')
    digestions= fields.Char(string='Digestiones')
    dietary_supplement = fields.Char(string='Comp. alimenticio')
    te = fields.Boolean('Te')
    te_cups = fields.Integer(string='Tazas por día')
    
    
    #AÑADO CAMPOS QUE SE INCORPORAN A INFORMACIÓN GENERAL
    blood_pressure = fields.Char(string='Tensión arterial')
    operations = fields.Char(string='Operaciones')
    aesthetic_operations = fields.Char(string='Operaciones de estética')
    origin = fields.Selection([('w','Web'),('v','Venta física'),('e','Evento'),('o','Otros')],string='Procedencia')
    date_admitted = fields.Date(string="Fecha alta", default=lambda self: fields.Date.today())

    #AÑADO CAMPOS A ESTILO DE VIDA->ADICCIONES
    smoking_comments = fields.Char(string='Comentario tabaco')
    alcohol_comments = fields.Char(string='Comentario alcohol')

    #AÑADO NOTEBOOK Y CAMPOS DENTRO DE ENFERMEDADES, VISTA ALTERACIONES CIRCULATORIAS
    cold_hands_and_feet = fields.Boolean(string="Pies y manos frías")
    chilblains= fields.Boolean(string="Sabañones")
    haviness_legs = fields.Boolean(string="Pesadez piernas")
    ankle_haviness = fields.Boolean(string="Pesadez tobillos")
    tingling = fields.Boolean(string="Hormigueos")
    edema = fields.Boolean(string="Edema extr. inferiores")        
    varicose_veins = fields.Boolean(string="Varices")

    #AÑADO CAMPOS QUE SE INCORPORAN A GINECO/OBSERVACIONES MÉDICAS
    menstrual_cycles = fields.Selection([('r', 'Regular'),('i', 'Irregular')], string ="Ciclos menstruales")
    days_of_menstruation = fields.Integer('Número de días')
    menstrual_type = fields.Selection([('n', 'Normal'),('a', 'Abundante')], string ="Tipo de menstruación")
    menstrual_comments = fields.Char(string='Comentarios')

    #AÑADO NOTEBOOK Y CAMPOS ANALISIS ESTETICO FACIAL DENTRO DE INFORMACIÓN GENERAL**************
    #Campos Tipo de piel
    thin_skin = fields.Boolean(string="Fina")
    normal_skin = fields.Boolean(string="Normal")
    thick_skin = fields.Boolean(string="Gruesa")
    dry_skin = fields.Boolean(string="Seca")
    mixed_skin = fields.Boolean(string="Mixta")
    dehydrated_skin = fields.Boolean(string="Deshidratada")
    poisoned_skin = fields.Boolean(string="Intoxicada")
    oily_skin = fields.Boolean(string="Grasa")
    devitalized_skin = fields.Boolean(string="Desvitalizada")
    sensitive_skin = fields.Boolean(string="Sensible")
    acneic_skin = fields.Boolean(string="Acneica")
    comments_skin= fields.Text(string="Comentario")

    #Campos Inesteticismos faciales
    wrinkles = fields.Boolean(string="Arrugas")
    asphyctic = fields.Boolean(string="Asfíctica")
    pores= fields.Boolean(string="Poros")
    coupe= fields.Boolean(string="Coupe")
    acne= fields.Boolean(string="Acné")
    flaccidity = fields.Boolean(string="Flacidez")
    ptosis = fields.Boolean(string="Ptosis")
    fragile = fields.Boolean(string="Frágil")
    comedones = fields.Boolean(string="Comedones")
    tallow = fields.Boolean(string="Sebo")
    millums = fields.Boolean(string="Millums")
    reactive = fields.Boolean(string="Reactiva")
    
    #Campos Dilatación de poros
    normal = fields.Boolean(string="Normal")
    dilated = fields.Boolean(string="Dilatados")
    very_dilated= fields.Boolean(string="Muy dilatados")
    
    #Campos Alteraciones microcirculación
    erythrosis= fields.Boolean(string="Enroj. o eritrosis")
    dilated_capillaries = fields.Boolean(string="Capilares dilatados")
    caparrosa= fields.Boolean(string="Caparrosa")
    
    #Campos Manchas en la piel
    dark= fields.Boolean(string="Oscuras")
    clear = fields.Boolean(string="Claras")
    lack_of_pigmentation= fields.Boolean(string="Falta de pigmentación")
    
    #Campos Flacidez
    in_the_face= fields.Boolean(string="En el rostro")
    in_the_eloval = fields.Boolean(string="En el elóovalo")
    in_the_neck= fields.Boolean(string="En el cuello")
 
    #Campos Alteraciones general de la piel
    pupulas= fields.Boolean(string="Púpulas")
    papules = fields.Boolean(string="Pápulas")
    scars= fields.Boolean(string="Cicatrices")
    brands = fields.Boolean(string="Marcas")
    hair_in_the_face= fields.Boolean(string="Vellos en el rostro")
    
    #Campos Respuestas de la piel al sol o fototipos cutáneos
    red_skin= fields.Boolean(string="Se enrojece y no se broncea")
    pigmented_skin = fields.Boolean(string="Se enrojece y después se broncea")
    tan_skin= fields.Boolean(string="Se broncea")

    #Campos Arrugas y líneas
    around_mouth_and_eyes= fields.Boolean(string="Sólo alrededor de boca y ojos")
    forehead = fields.Boolean(string="Frente")
    glabella= fields.Boolean(string="Glavela")
    nasolabial_folds = fields.Boolean(string="Surcos nasogenianos")
    
    #Campos Contorno de ojos
    bags= fields.Boolean(string="Bolsas")
    baggy_eyes = fields.Boolean(string="Ojeras")
    wrinkles_eye= fields.Boolean(string="Arrugas")
    sagging_upper_eyelid = fields.Boolean(string="Flac.párpado superior")
    
    #Campos Pelos supérfluos
    normal_hairs= fields.Boolean(string="Normal")
    hirsutism = fields.Boolean(string="Hirsutismo")
    hypertrichosis= fields.Boolean(string="Hipertricosis")
    location = fields.Char(string="Localización")
    type_hair_removal = fields.Char(string ="Tipo depilación")
    
    #Campos Tratamiento facial
    treatment_facial = fields.Text(string="Tratamiento")
    sesions_facial = fields.Integer(string="Número de sesiones")
    frequency_facial = fields.Char(string="Frecuencia")
    start_treatment_facial = fields.Date(string="Inicio tratamiento")
    end_treatment_facial = fields.Date(string="Fin tratamiento")
    
    #Campos Tratamiento domiciliario
    morning_facial = fields.Text(string="Mañana")
    night_facial = fields.Text(string="Noche")
    spullements_facial = fields.Text(string="Suplementos")
    recommended_facial = fields.Text(string="Recomiendo")

    #Campos Medicina estética
    aesthetic_medicine_facial = fields.Text(string="Medicina estética")


     #AÑADO NOTEBOOK Y CAMPOS ANALISIS ESTETICO CORPORAL DENTRO DE INFORMACIÓN GENERAL**************
    #Campos Tejidos
    compacted= fields.Boolean(string="Compactada")
    relaxed= fields.Boolean(string="Relajada")
    desigual= fields.Boolean(string="Desigual")
    edematous_tissue = fields.Boolean(string="Edematosa")

    #Campos Adiposidad
    adiposity_location= fields.Text(string="Localización")
   
    #Campos Celulitis
    edematous_cellulitis= fields.Boolean(string="Edematosa")
    fibrous_cellulitis = fields.Boolean(string="Fibrosa")
    sclera_cellulitis= fields.Boolean(string="Esclerótica")
    location_cellulitis = fields.Text(string="Localización")

    #Campos Flacidez
    light_sagging= fields.Boolean(string="Ligera")
    medium_sagging = fields.Boolean(string="Media")
    hard_sagging= fields.Boolean(string="Fuerte")
    muscle_sagging = fields.Boolean(string="Muscular")
    location_sagging = fields.Text(string="Localización")

    #Campos Estrías
    white_stretch_marks= fields.Boolean(string="Blancas")
    pink_strech_marks = fields.Boolean(string="Rosadas")
    location_strech_marks= fields.Text(string="Localización")
    
    #Campos Peso
    actual_weight= fields.Integer(string="Actual")
    ideal_weight = fields.Integer(string="Ideal")
    desired_weight= fields.Integer(string="Deseado")
    imc_weight= fields.Integer(string="I.M.C.")
    muscle_weight = fields.Integer(string="Músculo")
    fat_weight= fields.Integer(string="Grasa")
    visceral_fat = fields.Integer(string="Grasa visceral")

    #Campos Medidas
    waist_start_tratment= fields.Integer(string="Cintura")
    hips_start_treatment= fields.Integer(string="Caderas")
    nalgas_start_treatment= fields.Integer(string="Nalgas")
    buttocks_start_treatment= fields.Integer(string="Gluteos")
    thighs_start_treatment= fields.Integer(string="Muslos")
    knees_start_treatment= fields.Integer(string="Rodillas")
    calves_start_treatment= fields.Integer(string="Pantorrillas")
    unkle_start_treatment = fields.Integer(string="Tobillos")
    
    waist_end_tratment= fields.Integer(string="Cintura")
    hips_end_treatment= fields.Integer(string="Caderas")
    nalgas_end_treatment= fields.Integer(string="Nalgas")
    buttocks_end_treatment= fields.Integer(string="Gluteos")
    thighs_end_treatment= fields.Integer(string="Muslos")
    knees_end_treatment= fields.Integer(string="Rodillas")
    calves_end_treatment= fields.Integer(string="Pantorrillas")
    unkle_end_treatment = fields.Integer(string="Tobillos")
    
    #Campos Tratamiento corporal
    treatment_corporal = fields.Text(string="Tratamiento")
    sesions_corporal = fields.Integer(string="Número de sesiones")
    frequency_corporal = fields.Char(string="Frecuencia")
    start_treatment_corporal = fields.Date(string="Inicio tratamiento")
    end_treatment_corporal = fields.Date("Fin tratamiento")

    #Campos Tratamiento domiciliario
    morning_corporal = fields.Text(string="Mañana")
    night_corporal = fields.Text(string="Noche")
    spullements_corporal = fields.Text(string="Suplementos")
    recommended_corporal = fields.Text(string="Recomiendo")

    #Campos Medicina estética corportal
    aesthetic_medicine_corporal = fields.Text(string="Medicina estética")

    def _valid_field_parameter(self, field, name):
        return name == 'sort' or super()._valid_field_parameter(field, name)

    @api.model_create_multi
    def create(self,vals_list):
        for val in vals_list:
            appointment = self._context.get('appointment_id')
            res_partner_obj = self.env['res.partner']
            if appointment:
                val_1 = {'name': self.env['res.partner'].browse(val['patient_id']).name}
                patient= res_partner_obj.create(val_1)
                val.update({'patient_id': patient.id})
            if val.get('date_of_birth'):
                dt = val.get('date_of_birth')
                d1 = datetime.strptime(str(dt), "%Y-%m-%d").date()
                d2 = datetime.today().date()
                rd = relativedelta(d2, d1)
                age = str(rd.years) + "y" +" "+ str(rd.months) + "m" +" "+ str(rd.days) + "d"
                val.update({'age':age} )

            patient_id  = self.env['ir.sequence'].next_by_code('medical.patient')
            if patient_id:
                val.update({
                            'name':patient_id,
                           })
           
        return super(medical_patient, self).create(vals_list)

    @api.constrains('date_of_death')
    def _check_date_death(self):
        for rec in self:
            if rec.date_of_birth:
                if rec.deceased == True :
                    if rec.date_of_death <= rec.date_of_birth :
                      raise UserError(_('Date Of Death Can Not Less Than Date Of Birth.' ))

    def copy(self, default=None):
        for rec in self:
            raise UserError(_('You Can Not Duplicate Patient.' ))

# vim=expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
