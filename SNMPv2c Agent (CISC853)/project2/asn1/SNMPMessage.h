/*
 * Generated by asn1c-0.9.21 (http://lionet.info/asn1c)
 * From ASN.1 module "MyTest"
 * 	found in "../MyTest.asn1"
 * 	`asn1c -fnative-types`
 */

#ifndef	_SNMPMessage_H_
#define	_SNMPMessage_H_


#include <asn_application.h>

/* Including external dependencies */
#include <NativeInteger.h>
#include <OCTET_STRING.h>
#include "PDUs.h"
#include <constr_SEQUENCE.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Dependencies */
typedef enum version {
	version_version	= 1
} e_version;

/* SNMPMessage */
typedef struct SNMPMessage {
	long	 version;
	OCTET_STRING_t	 community;
	PDUs_t	 data;
	
	/* Context for parsing across buffer boundaries */
	asn_struct_ctx_t _asn_ctx;
} SNMPMessage_t;

/* Implementation */
extern asn_TYPE_descriptor_t asn_DEF_SNMPMessage;

#ifdef __cplusplus
}
#endif

#endif	/* _SNMPMessage_H_ */
