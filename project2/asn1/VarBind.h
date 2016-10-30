/*
 * Generated by asn1c-0.9.21 (http://lionet.info/asn1c)
 * From ASN.1 module "MyTest"
 * 	found in "../MyTest.asn1"
 * 	`asn1c -fnative-types`
 */

#ifndef	_VarBind_H_
#define	_VarBind_H_


#include <asn_application.h>

/* Including external dependencies */
#include "ObjectName.h"
#include "ObjectSyntax.h"
#include <NULL.h>
#include <constr_CHOICE.h>
#include <constr_SEQUENCE.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Dependencies */
typedef enum choice_PR {
	choice_PR_NOTHING,	/* No components present */
	choice_PR_value,
	choice_PR_unSpecified,
	choice_PR_noSuchObject,
	choice_PR_noSuchInstance,
	choice_PR_endOfMibView
} choice_PR;

/* VarBind */
typedef struct VarBind {
	ObjectName_t	 name;
	struct choice {
		choice_PR present;
		union VarBind__choice_u {
			ObjectSyntax_t	 value;
			NULL_t	 unSpecified;
			NULL_t	 noSuchObject;
			NULL_t	 noSuchInstance;
			NULL_t	 endOfMibView;
		} choice;
		
		/* Context for parsing across buffer boundaries */
		asn_struct_ctx_t _asn_ctx;
	} choice;
	
	/* Context for parsing across buffer boundaries */
	asn_struct_ctx_t _asn_ctx;
} VarBind_t;

/* Implementation */
extern asn_TYPE_descriptor_t asn_DEF_VarBind;

#ifdef __cplusplus
}
#endif

#endif	/* _VarBind_H_ */
