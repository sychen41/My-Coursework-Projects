/*
 * Generated by asn1c-0.9.21 (http://lionet.info/asn1c)
 * From ASN.1 module "MyTest"
 * 	found in "../MyTest.asn1"
 * 	`asn1c -fnative-types`
 */

#ifndef	_InformRequest_PDU_H_
#define	_InformRequest_PDU_H_


#include <asn_application.h>

/* Including external dependencies */
#include "PDU.h"

#ifdef __cplusplus
extern "C" {
#endif

/* InformRequest-PDU */
typedef PDU_t	 InformRequest_PDU_t;

/* Implementation */
extern asn_TYPE_descriptor_t asn_DEF_InformRequest_PDU;
asn_struct_free_f InformRequest_PDU_free;
asn_struct_print_f InformRequest_PDU_print;
asn_constr_check_f InformRequest_PDU_constraint;
ber_type_decoder_f InformRequest_PDU_decode_ber;
der_type_encoder_f InformRequest_PDU_encode_der;
xer_type_decoder_f InformRequest_PDU_decode_xer;
xer_type_encoder_f InformRequest_PDU_encode_xer;

#ifdef __cplusplus
}
#endif

#endif	/* _InformRequest_PDU_H_ */
